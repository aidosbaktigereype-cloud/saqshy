from django.core.management.base import BaseCommand

from crm.reminders import send_due


class Command(BaseCommand):
    help = "Отправляет в Telegram напоминания по заявкам, у которых наступил «следующий шаг»."

    def handle(self, *args, **options):
        sent = send_due()
        if options.get("verbosity", 1) > 1 or sent:
            self.stdout.write(f"Напоминаний отправлено: {sent}")
