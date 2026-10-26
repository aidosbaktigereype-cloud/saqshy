import secrets

from django.conf import settings
from django.db import models, transaction


class LeadStatus(models.TextChoices):
    NEW = "new", "Новая"
    IN_WORK = "in_work", "В работе"
    MEASURE = "measure", "Замер назначен"
    PROPOSAL = "proposal", "КП отправлено"
    INSTALL = "install", "Монтаж"
    DONE = "done", "Завершена"
    LOST = "lost", "Отказ"


OPEN_STATUSES = [
    LeadStatus.NEW,
    LeadStatus.IN_WORK,
    LeadStatus.MEASURE,
    LeadStatus.PROPOSAL,
    LeadStatus.INSTALL,
]


class LeadSource(models.TextChoices):
    FORM = "form", "Форма на сайте"
    CALLBACK = "callback", "Обратный звонок"
    QUIZ = "quiz", "Квиз"
    PHONE = "phone", "Звонок"
    MESSENGER = "messenger", "WhatsApp / Telegram"
    MANUAL = "manual", "Добавлена вручную"


class Lead(models.Model):
    name = models.CharField("Имя", max_length=120, blank=True)
    phone = models.CharField("Телефон", max_length=32)
    service = models.ForeignKey(
        "services.Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads",
        verbose_name="Услуга",
    )
    object_type = models.CharField("Тип объекта", max_length=120, blank=True)
    message = models.TextField("Комментарий клиента", blank=True)
    source = models.CharField("Канал", max_length=20, choices=LeadSource.choices, default=LeadSource.FORM)

    # Воронка
    status = models.CharField("Этап", max_length=20, choices=LeadStatus.choices, default=LeadStatus.NEW, db_index=True)
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads",
        verbose_name="Ответственный",
    )
    next_action_at = models.DateTimeField("Следующий шаг", null=True, blank=True)
    amount = models.PositiveIntegerField("Сумма сделки, ₸", null=True, blank=True)
    lost_reason = models.CharField("Причина отказа", max_length=200, blank=True)

    # Откуда пришёл клиент (нужно для рекламы и офлайн-конверсий)
    page_url = models.CharField("Страница", max_length=500, blank=True)
    locale = models.CharField("Язык", max_length=5, blank=True)
    utm_source = models.CharField(max_length=120, blank=True)
    utm_medium = models.CharField(max_length=120, blank=True)
    utm_campaign = models.CharField(max_length=200, blank=True)
    utm_content = models.CharField(max_length=200, blank=True)
    utm_term = models.CharField(max_length=200, blank=True)
    gclid = models.CharField(max_length=255, blank=True)
    yclid = models.CharField(max_length=255, blank=True)
    ym_client_id = models.CharField("ClientID Метрики", max_length=64, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)
    consent = models.BooleanField("Согласие на обработку ПДн", default=False)

    telegram_message_id = models.BigIntegerField(null=True, blank=True, editable=False)
    created_at = models.DateTimeField("Создана", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)

    # Фаза 5: здесь появятся связи customer и order (личный кабинет и заказы).

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "заявка"
        verbose_name_plural = "заявки"

    def __str__(self) -> str:
        return f"#{self.pk} {self.name or 'Без имени'} · {self.phone}"

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._remember_state()
        return instance

    def _remember_state(self) -> None:
        self._loaded = {"status": self.status, "assignee_id": self.assignee_id}

    @property
    def phone_digits(self) -> str:
        return "".join(ch for ch in self.phone if ch.isdigit())

    def save(self, *args, actor=None, **kwargs):
        """Сохраняет заявку и пишет в историю смену этапа и ответственного.

        actor — сотрудник, который сделал изменение (из админки или бота).
        """
        is_new = self._state.adding
        loaded = getattr(self, "_loaded", None)
        super().save(*args, **kwargs)

        events = []
        if is_new:
            events.append((LeadEvent.Kind.CREATED, f"Заявка создана: {self.get_source_display()}"))
        elif loaded:
            if loaded["status"] != self.status:
                old = LeadStatus(loaded["status"]).label
                events.append((LeadEvent.Kind.STATUS, f"{old} → {self.get_status_display()}"))
            if loaded["assignee_id"] != self.assignee_id:
                who = (self.assignee.get_full_name() or self.assignee.username) if self.assignee else "никто"
                events.append((LeadEvent.Kind.ASSIGN, f"Ответственный: {who}"))
        for kind, text in events:
            LeadEvent.objects.create(lead=self, kind=kind, text=text, author=actor)
        self._remember_state()

        if events and not is_new:
            # Обновляем карточку заявки в Telegram после коммита транзакции.
            from crm import telegram

            transaction.on_commit(lambda: telegram.refresh_lead_message_async(self.pk))


class LeadEvent(models.Model):
    class Kind(models.TextChoices):
        CREATED = "created", "Создана"
        STATUS = "status", "Смена этапа"
        ASSIGN = "assign", "Назначение"
        COMMENT = "comment", "Комментарий"

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="events", verbose_name="Заявка")
    kind = models.CharField("Тип", max_length=20, choices=Kind.choices)
    text = models.TextField("Текст", blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автор"
    )
    created_at = models.DateTimeField("Когда", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "событие"
        verbose_name_plural = "история заявок"

    def __str__(self) -> str:
        return f"{self.get_kind_display()}: {self.text[:60]}"


def new_link_code() -> str:
    return secrets.token_hex(4).upper()


class StaffProfile(models.Model):
    """Telegram-привязка сотрудника. Бот отвечает только привязанным аккаунтам."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="staff_profile", verbose_name="Сотрудник"
    )
    telegram_id = models.BigIntegerField("Telegram ID", null=True, blank=True, unique=True)
    telegram_username = models.CharField("Telegram username", max_length=64, blank=True)
    link_code = models.CharField(
        "Код привязки",
        max_length=16,
        default=new_link_code,
        unique=True,
        help_text="Отправьте боту команду /link КОД, чтобы привязать Telegram",
    )

    class Meta:
        verbose_name = "профиль сотрудника"
        verbose_name_plural = "профили сотрудников"

    def __str__(self) -> str:
        return f"{self.user} (tg: {self.telegram_username or self.telegram_id or '—'})"
