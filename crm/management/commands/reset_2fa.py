from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django_otp.plugins.otp_totp.models import TOTPDevice


class Command(BaseCommand):
    help = "Сбрасывает 2FA сотрудника (например, если потерян телефон). При следующем входе он настроит её заново."

    def add_arguments(self, parser):
        parser.add_argument("username")

    def handle(self, *args, username: str, **options):
        user = get_user_model().objects.filter(username=username).first()
        if not user:
            raise CommandError(f"Пользователь {username} не найден")
        deleted, _ = TOTPDevice.objects.filter(user=user).delete()
        self.stdout.write(self.style.SUCCESS(f"2FA сброшена для {username} (удалено устройств: {deleted})"))
