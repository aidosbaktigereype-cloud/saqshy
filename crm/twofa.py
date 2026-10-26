"""Двухфакторная защита входа в CRM: TOTP-коды из Google Authenticator, Яндекс Ключа и т.п."""

import base64
from io import BytesIO

import qrcode
import qrcode.image.svg
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.safestring import mark_safe
from django_otp import login as otp_login
from django_otp import match_token
from django_otp.plugins.otp_totp.models import TOTPDevice

LOGIN_URL = "/crm/login/"


def qr_svg(data: str) -> str:
    image = qrcode.make(data, image_factory=qrcode.image.svg.SvgPathImage, box_size=8, border=2)
    buffer = BytesIO()
    image.save(buffer)
    return buffer.getvalue().decode()


def clean_token(raw: str) -> str:
    return "".join(ch for ch in (raw or "") if ch.isdigit())


def safe_next(request, default: str = "/crm/") -> str:
    target = request.POST.get("next") or request.GET.get("next") or default
    if url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return target
    return default


def context(request, **extra):
    return {**admin.site.each_context(request), **extra}


@login_required(login_url=LOGIN_URL)
def setup(request):
    user = request.user
    if not user.is_staff:
        return redirect(LOGIN_URL)
    confirmed = TOTPDevice.objects.filter(user=user, confirmed=True).first()
    if confirmed:
        return render(request, "crm/2fa_setup.html", context(request, title="Двухфакторная защита", enabled=True))

    device = TOTPDevice.objects.filter(user=user, confirmed=False).first() or TOTPDevice.objects.create(
        user=user, name="Приложение-аутентификатор", confirmed=False
    )
    error = ""
    if request.method == "POST":
        if device.verify_token(clean_token(request.POST.get("token"))):
            device.confirmed = True
            device.save(update_fields=["confirmed"])
            otp_login(request, device)
            return redirect("/crm/")
        error = "Код не подошёл. Проверьте время на телефоне и введите новый код."

    secret = base64.b32encode(device.bin_key).decode()
    return render(
        request,
        "crm/2fa_setup.html",
        context(
            request,
            title="Настройка двухфакторной защиты",
            enabled=False,
            qr=mark_safe(qr_svg(device.config_url)),
            secret=" ".join(secret[i : i + 4] for i in range(0, len(secret), 4)),
            error=error,
            required=settings.ADMIN_2FA_REQUIRED and user.is_superuser,
        ),
    )


@login_required(login_url=LOGIN_URL)
def verify(request):
    if request.user.is_verified():
        return redirect(safe_next(request))
    error = ""
    if request.method == "POST":
        device = match_token(request.user, clean_token(request.POST.get("token")))
        if device:
            otp_login(request, device)
            return redirect(safe_next(request))
        error = "Неверный или устаревший код."
    return render(
        request,
        "crm/2fa_verify.html",
        context(request, title="Код подтверждения", error=error, next=safe_next(request)),
    )
