"""WhatsApp Business Cloud API (Meta): входящие сообщения → заявки в CRM, ответы клиенту.

Документация: https://developers.facebook.com/docs/whatsapp/cloud-api
Ответить произвольным текстом можно в течение 24 часов после последнего сообщения клиента.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
from datetime import timedelta

import requests
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)
REPLY_WINDOW = timedelta(hours=24)


def enabled() -> bool:
    return bool(settings.WHATSAPP_TOKEN and settings.WHATSAPP_PHONE_NUMBER_ID)


def verify_signature(body: bytes, header: str) -> bool:
    """Проверяет X-Hub-Signature-256: HMAC-SHA256 тела запроса ключом App Secret."""
    secret = settings.WHATSAPP_APP_SECRET
    if not secret:
        return settings.DEBUG  # без секрета принимаем вебхуки только в режиме разработки
    expected = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header or "")


def send_text(to_digits: str, text: str) -> str | None:
    """Отправляет текст клиенту. Возвращает ID сообщения WhatsApp или None при ошибке."""
    if not enabled():
        return None
    url = f"https://graph.facebook.com/{settings.WHATSAPP_API_VERSION}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    try:
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {settings.WHATSAPP_TOKEN}"},
            json={"messaging_product": "whatsapp", "to": to_digits, "type": "text", "text": {"body": text[:4096]}},
            timeout=15,
        )
        data = response.json()
    except (requests.RequestException, ValueError):
        logger.exception("WhatsApp send failed")
        return None
    if response.status_code >= 400:
        logger.warning("WhatsApp send error: %s", data.get("error"))
        return None
    return (data.get("messages") or [{}])[0].get("id")


def last_inbound_at(lead):
    from crm.models import Message

    message = lead.messages.filter(direction=Message.Direction.IN).order_by("-created_at").first()
    return message.created_at if message else None


def can_reply(lead) -> bool:
    last = last_inbound_at(lead)
    return bool(last and timezone.now() - last < REPLY_WINDOW)


def reply(lead, text: str, author=None) -> tuple[bool, str]:
    """Отвечает клиенту от имени компании и сохраняет сообщение в переписке."""
    from crm.models import Message

    if not enabled():
        return False, "WhatsApp не подключён (нет WHATSAPP_TOKEN)"
    if not can_reply(lead):
        return False, "Прошло больше 24 часов с последнего сообщения клиента — свободный ответ запрещён правилами WhatsApp"
    external_id = send_text(lead.phone_digits, text)
    if not external_id:
        return False, "WhatsApp не принял сообщение, подробности в логах"
    Message.objects.create(
        lead=lead, direction=Message.Direction.OUT, text=text, external_id=external_id, author=author
    )
    return True, "Отправлено в WhatsApp"


def message_text(message: dict) -> str:
    kind = message.get("type")
    if kind == "text":
        return message.get("text", {}).get("body", "")
    if kind in {"button", "interactive"}:
        payload = message.get(kind, {})
        return payload.get("text") or str(payload)[:500]
    caption = (message.get(kind) or {}).get("caption", "")
    return f"[{kind}] {caption}".strip()


def handle_webhook(payload: dict) -> int:
    """Разбирает вебхук Meta. Возвращает число обработанных входящих сообщений."""
    count = 0
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            names = {c.get("wa_id"): (c.get("profile") or {}).get("name", "") for c in value.get("contacts", [])}
            for message in value.get("messages", []):
                sender = message.get("from", "")
                if process_incoming(sender, names.get(sender, ""), message_text(message), message.get("id", "")):
                    count += 1
    return count


def process_incoming(wa_id: str, name: str, text: str, external_id: str) -> bool:
    from crm import telegram
    from crm.models import OPEN_STATUSES, Lead, LeadSource, Message
    from crm.views import normalize_phone

    if external_id and Message.objects.filter(external_id=external_id).exists():
        return False  # Meta иногда присылает одно и то же сообщение повторно
    phone = normalize_phone(wa_id)
    if not phone:
        return False

    lead = Lead.objects.filter(phone=phone, status__in=OPEN_STATUSES).order_by("-created_at").first()
    is_new = lead is None
    if is_new:
        lead = Lead.objects.create(
            name=name[:120], phone=phone, source=LeadSource.MESSENGER, message=text[:2000], consent=True, locale=""
        )
    message = Message.objects.create(lead=lead, direction=Message.Direction.IN, text=text, external_id=external_id)

    if is_new:
        telegram.notify_new_lead_async(lead.pk)
    else:
        telegram.notify_message_async(message.pk)
    return True
