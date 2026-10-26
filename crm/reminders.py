"""Напоминания о «следующем шаге» по заявкам.

Запускается командой `python manage.py send_reminders` (cron раз в минуту на сервере)
и автоматически внутри `telegram_poll` при локальной разработке.
"""

from django.db.models import F, Q
from django.utils import timezone

from crm import telegram
from crm.models import OPEN_STATUSES, Lead


def due_leads(now=None):
    now = now or timezone.now()
    return (
        Lead.objects.filter(status__in=OPEN_STATUSES, next_action_at__lte=now)
        .filter(Q(reminder_sent_at__isnull=True) | Q(reminder_sent_at__lt=F("next_action_at")))
        .select_related("assignee__staff_profile", "service")
    )


def send_due(now=None) -> int:
    now = now or timezone.now()
    sent = 0
    for lead in due_leads(now):
        if telegram.send_reminder(lead):
            sent += 1
        # Отмечаем даже при неудаче, чтобы не слать одно и то же каждую минуту.
        Lead.objects.filter(pk=lead.pk).update(reminder_sent_at=now)
    return sent
