from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from crm import telegram


class Command(BaseCommand):
    help = "Регистрирует вебхук бота на SITE_URL/tg/webhook/ (нужен публичный HTTPS)."

    def handle(self, *args, **options):
        if not (settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_WEBHOOK_SECRET):
            raise CommandError("Нужны TELEGRAM_BOT_TOKEN и TELEGRAM_WEBHOOK_SECRET в .env")
        if not settings.SITE_URL.startswith("https://"):
            raise CommandError("SITE_URL должен начинаться с https:// — Telegram не принимает HTTP-вебхуки")
        url = f"{settings.SITE_URL}/tg/webhook/"
        result = telegram.call(
            "setWebhook",
            url=url,
            secret_token=settings.TELEGRAM_WEBHOOK_SECRET,
            allowed_updates=["message", "callback_query"],
        )
        if result is None:
            raise CommandError("Telegram не принял вебхук — проверьте токен и логи")
        telegram.call(
            "setMyCommands",
            commands=[
                {"command": "new", "description": "Новые заявки без ответственного"},
                {"command": "today", "description": "Мои открытые заявки"},
                {"command": "link", "description": "Привязать аккаунт: /link КОД"},
            ],
        )
        self.stdout.write(self.style.SUCCESS(f"Вебхук установлен: {url}"))
