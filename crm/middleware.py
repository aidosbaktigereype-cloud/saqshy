from django.conf import settings
from django.shortcuts import redirect
from django.utils import translation
from django.utils.http import urlencode
from django_otp.plugins.otp_totp.models import TOTPDevice

ADMIN_PREFIX = "/crm/"
TWO_FA_EXEMPT = ("/crm/login/", "/crm/logout/", "/crm/2fa/", "/crm/jsi18n/")


class AdminRussianMiddleware:
    """CRM всегда на русском, независимо от языка браузера сотрудника."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(ADMIN_PREFIX):
            translation.activate("ru")
            request.LANGUAGE_CODE = "ru"
        return self.get_response(request)


class AdminTwoFactorMiddleware:
    """Требует код из приложения-аутентификатора при входе в CRM.

    Если у сотрудника настроена 2FA — просим код. Суперпользователей без 2FA
    (при ADMIN_2FA_REQUIRED=1) отправляем на страницу настройки.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        user = getattr(request, "user", None)
        if (
            path.startswith(ADMIN_PREFIX)
            and not path.startswith(TWO_FA_EXEMPT)
            and user is not None
            and user.is_authenticated
            and user.is_staff
            and not user.is_verified()
        ):
            has_device = TOTPDevice.objects.filter(user=user, confirmed=True).exists()
            if has_device:
                return redirect("/crm/2fa/verify/?" + urlencode({"next": request.get_full_path()}))
            if settings.ADMIN_2FA_REQUIRED and user.is_superuser:
                return redirect("/crm/2fa/setup/")
        return self.get_response(request)
