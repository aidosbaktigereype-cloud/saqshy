import html
import json
import logging
import re

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from crm import telegram
from crm.models import Lead, LeadSource
from services.models import Service

logger = logging.getLogger(__name__)

TRACKING_FIELDS = (
    "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "gclid", "yclid", "ym_client_id",
)


def normalize_phone(raw: str) -> str | None:
    """Приводит номер к виду +7 777 123 45 67. Иностранные номера оставляет как есть."""
    digits = re.sub(r"\D", "", raw or "")
    if len(digits) == 11 and digits[0] in "78":
        digits = "7" + digits[1:]
    elif len(digits) == 10:
        digits = "7" + digits
    if len(digits) == 11 and digits.startswith("7"):
        return f"+7 {digits[1:4]} {digits[4:7]} {digits[7:9]} {digits[9:11]}"
    if 10 <= len(digits) <= 15:
        return f"+{digits}"
    return None


def client_ip(request: HttpRequest) -> str | None:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    return forwarded.split(",")[0].strip() or request.META.get("REMOTE_ADDR")


def wants_json(request: HttpRequest) -> bool:
    return "application/json" in request.headers.get("Accept", "") or request.content_type == "application/json"


def read_payload(request: HttpRequest) -> dict:
    if request.content_type == "application/json":
        try:
            data = json.loads(request.body or b"{}")
            return data if isinstance(data, dict) else {}
        except ValueError:
            return {}
    return request.POST.dict()


def rate_limited(ip: str | None) -> bool:
    key = f"lead-rate:{ip or 'unknown'}"
    count = cache.get(key, 0)
    if count >= settings.LEAD_RATE_LIMIT:
        return True
    cache.set(key, count + 1, settings.LEAD_RATE_WINDOW)
    return False


def respond(request: HttpRequest, ok: bool, locale: str, errors: dict | None = None, status: int = 200):
    if wants_json(request):
        return JsonResponse({"ok": ok, "errors": errors or {}}, status=status)
    if ok:
        with translation.override(locale):
            return redirect(reverse("thanks"))
    return HttpResponse("Проверьте телефон и согласие на обработку данных.", status=status)


@require_POST
def lead_create(request: HttpRequest):
    data = read_payload(request)
    locale = data.get("locale") if data.get("locale") in dict(settings.LANGUAGES) else "ru"

    # Скрытое поле-ловушка: люди его не видят, боты заполняют. Делаем вид, что всё хорошо.
    if str(data.get("website", "")).strip():
        return respond(request, True, locale)

    ip = client_ip(request)
    if rate_limited(ip):
        return respond(request, False, locale, {"__all__": "too_many"}, status=429)

    errors = {}
    phone = normalize_phone(str(data.get("phone", "")))
    if not phone:
        errors["phone"] = "invalid"
    if str(data.get("consent", "")).lower() not in {"1", "true", "on", "yes"}:
        errors["consent"] = "required"
    if errors:
        return respond(request, False, locale, errors, status=400)

    source = data.get("source") if data.get("source") in LeadSource.values else LeadSource.FORM
    service = Service.objects.filter(slug=str(data.get("service", ""))[:50], is_active=True).first()

    lead = Lead.objects.create(
        name=str(data.get("name", "")).strip()[:120],
        phone=phone,
        service=service,
        object_type=str(data.get("object_type", "")).strip()[:120],
        message=str(data.get("message", "")).strip()[:2000],
        source=source,
        page_url=str(data.get("page", ""))[:500],
        locale=locale,
        ip=ip,
        user_agent=request.headers.get("User-Agent", "")[:300],
        consent=True,
        **{field: str(data.get(field, ""))[:250] for field in TRACKING_FIELDS},
    )
    transaction.on_commit(lambda: telegram.notify_new_lead_async(lead.pk))
    transaction.on_commit(lambda: send_lead_email(lead))
    return respond(request, True, locale)


def send_lead_email(lead: Lead) -> None:
    if not settings.LEAD_NOTIFY_EMAILS:
        return
    try:
        send_mail(
            subject=f"Новая заявка #{lead.pk} — {lead.phone}",
            message=html.unescape(re.sub(r"<[^>]+>", "", telegram.lead_text(lead))),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.LEAD_NOTIFY_EMAILS,
            fail_silently=True,
        )
    except Exception:  # почта не должна ломать приём заявки
        logger.exception("Lead email failed")


@csrf_exempt
@require_POST
def telegram_webhook(request: HttpRequest):
    secret = settings.TELEGRAM_WEBHOOK_SECRET
    if not secret or request.headers.get("X-Telegram-Bot-Api-Secret-Token") != secret:
        return HttpResponse(status=403)
    try:
        update = json.loads(request.body or b"{}")
    except ValueError:
        return HttpResponse(status=400)
    try:
        telegram.handle_update(update)
    except Exception:  # Telegram повторяет запрос при ошибке — отвечаем 200, ошибку логируем
        logger.exception("Telegram update failed")
    return HttpResponse("ok")
