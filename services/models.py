from django.db import models
from django.urls import reverse


def split_lines(text: str) -> list[str]:
    return [line.strip(" -•\t") for line in (text or "").splitlines() if line.strip()]


class Service(models.Model):
    class Icon(models.TextChoices):
        HUB = "hub", "Хаб / AJAX"
        CAMERA = "camera", "Камера"
        ACCESS = "access", "Доступ / СКУД"
        ALARM = "alarm", "Сирена / сигнализация"
        NETWORK = "network", "Сеть / слаботочка"

    slug = models.SlugField("URL", unique=True, help_text="Латиницей, например: ajax")
    icon = models.CharField("Иконка", max_length=20, choices=Icon.choices, default=Icon.HUB)
    title = models.CharField("Название (меню, карточки)", max_length=120)
    h1 = models.CharField("Заголовок H1", max_length=200)
    offer = models.CharField("Оффер под заголовком", max_length=300, blank=True)
    summary = models.TextField("Короткое описание (карточка)", blank=True)
    intro = models.TextField("Вводный текст на странице", blank=True)
    benefits = models.TextField("Преимущества (по одному на строку)", blank=True)
    object_types = models.TextField("Для каких объектов (по одному на строку)", blank=True)
    price_from = models.PositiveIntegerField("Цена «от», ₸", null=True, blank=True)
    seo_title = models.CharField("SEO title", max_length=200, blank=True)
    seo_description = models.CharField("SEO description", max_length=300, blank=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Опубликована", default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "услуга"
        verbose_name_plural = "услуги"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("service_detail", kwargs={"slug": self.slug})

    @property
    def benefit_list(self) -> list[str]:
        return split_lines(self.benefits)

    @property
    def object_list(self) -> list[str]:
        return split_lines(self.object_types)


class Package(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="packages", verbose_name="Услуга")
    name = models.CharField("Название", max_length=120)
    items = models.TextField("Состав (по одному на строку)")
    price_from = models.PositiveIntegerField("Цена «от», ₸", null=True, blank=True)
    price_note = models.CharField("Подпись к цене", max_length=80, blank=True, help_text="Например: «за точку» или «по замеру»")
    is_popular = models.BooleanField("Выделить как популярный", default=False)
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["service", "order", "id"]
        verbose_name = "пакет"
        verbose_name_plural = "пакеты"

    def __str__(self) -> str:
        return f"{self.service} — {self.name}"

    @property
    def item_list(self) -> list[str]:
        return split_lines(self.items)


class FAQ(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="faqs",
        null=True,
        blank=True,
        verbose_name="Услуга",
        help_text="Пусто — общий вопрос для главной страницы",
    )
    question = models.CharField("Вопрос", max_length=250)
    answer = models.TextField("Ответ")
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы и ответы"

    def __str__(self) -> str:
        return self.question
