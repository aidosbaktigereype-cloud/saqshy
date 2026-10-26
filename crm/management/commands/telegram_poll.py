import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from crm import telegram


class Command(BaseCommand):
    help = "Запускает бота в режиме long polling — для локальной разработки, где нет публичного HTTPS для вебхука."

    def handle(self, *args, **options):
        if not settings.TELEGRAM_BOT_TOKEN:
            raise CommandError("Укажите TELEGRAM_BOT_TOKEN в .env")
        telegram.call("deleteWebhook")
        me = telegram.call("getMe") or {}
        self.stdout.write(self.style.SUCCESS(f"Бот @{me.get('username', '?')} слушает обновления. Ctrl+C — выход."))
        offset = None
        while True:
            try:
                updates = telegram.call("getUpdates", timeout=25, offset=offset) or []
                for update in updates:
                    offset = update["update_id"] + 1
                    try:
                        telegram.handle_update(update)
                    except Exception as exc:  # одна плохая команда не должна ронять бота
                        self.stderr.write(f"Ошибка обработки: {exc}")
            except KeyboardInterrupt:
                break
            except Exception as exc:
                self.stderr.write(f"Сетевая ошибка: {exc}")
                time.sleep(3)
