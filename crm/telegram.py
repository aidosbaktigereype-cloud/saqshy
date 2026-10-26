"""Telegram-бот для сотрудников: уведомления о заявках и работа с ними кнопками.

Работает через Bot API напрямую (requests), без сторонних библиотек.
Продакшен — вебхук /tg/webhook/, локально — `python manage.py telegram_poll`.
"""

from __future__ import annotations

import html
import logging
import threading

import requests
from django.conf import settings
from django.db import close_old_connections
from django.utils import timezone

logger = logging.getLogger(__name__)
API = "https://api.telegram.org/bot{token}/{method}"

# Кнопки этапов в карточке заявки (код этапа, подпись).
STATUS_BUTTONS = [
    ("in_work", "📞 В работе"),
    ("measure", "📐 Замер"),
    ("proposal", "📄 КП"),
    ("install", "🔧 Монтаж"),
    ("done", "✅ Завершена"),
    ("lost", "❌ Отказ"),
]


def enabled() -> bool:
    return bool(settings.TELEGRAM_BOT_TOKEN)


def call(method: str, **payload) -> dict | None:
    if not enabled():
        return None
    try:
        response = requests.post(
            API.format(token=settings.TELEGRAM_BOT_TOKEN, method=method), json=payload, timeout=10
        )
        data = response.json()
        if not data.get("ok"):
            logger.warning("Telegram %s failed: %s", method, data.get("description"))
            return None
        return data.get("result")
    except (requests.RequestException, ValueError):
        logger.exception("Telegram %s request error", method)
        return None


def run_async(func, *args) -> None:
    """Отправка в фоне, чтобы форма на сайте не ждала ответа Telegram."""

    def target():
        try:
            func(*args)
        finally:
            close_old_connections()

    threading.Thread(target=target, daemon=True).start()


# --- Карточка заявки --------------------------------------------------------


def lead_text(lead) -> str:
    e = html.escape
    local_time = timezone.localtime(lead.created_at).strftime("%d.%m %H:%M")
    lines = [
        f"<b>Заявка #{lead.pk}</b> · {e(lead.get_status_display())}",
        f"👤 {e(lead.name or 'Без имени')}",
        f"📱 <code>{e(lead.phone)}</code>",
    ]
    if lead.service:
        lines.append(f"🛠 {e(lead.service.title)}")
    if lead.object_type:
        lines.append(f"🏠 {e(lead.object_type)}")
    if lead.message:
        lines.append(f"💬 {e(lead.message[:500])}")
    source = lead.get_source_display()
    if lead.utm_source:
        source += f" · {lead.utm_source}/{lead.utm_medium or '-'}"
    lines.append(f"🔎 {e(source)} · {lead.locale or 'ru'} · {local_time}")
    if lead.assignee:
        lines.append(f"🙋 Ответственный: {e(lead.assignee.get_full_name() or lead.assignee.username)}")
    if lead.amount:
        lines.append(f"💰 {lead.amount:,} ₸".replace(",", " "))
    return "\n".join(lines)


def lead_keyboard(lead) -> dict:
    rows = []
    if not lead.assignee_id:
        rows.append([{"text": "✋ Беру", "callback_data": f"lead:{lead.pk}:take"}])
    buttons = [
        {"text": label, "callback_data": f"lead:{lead.pk}:status:{code}"}
        for code, label in STATUS_BUTTONS
        if code != lead.status
    ]
    rows += [buttons[i : i + 3] for i in range(0, len(buttons), 3)]
    links = [{"text": "💬 WhatsApp", "url": f"https://wa.me/{lead.phone_digits}"}]
    admin_url = f"{settings.SITE_URL}/crm/crm/lead/{lead.pk}/change/"
    if admin_url.startswith("https://"):
        links.append({"text": "🗂 В CRM", "url": admin_url})
    rows.append(links)
    return {"inline_keyboard": rows}


def notify_new_lead(lead_id: int) -> None:
    from crm.models import Lead

    if not (enabled() and settings.TELEGRAM_CHAT_ID):
        return
    lead = Lead.objects.select_related("service", "assignee").get(pk=lead_id)
    result = call(
        "sendMessage",
        chat_id=settings.TELEGRAM_CHAT_ID,
        text=lead_text(lead),
        parse_mode="HTML",
        reply_markup=lead_keyboard(lead),
        disable_web_page_preview=True,
    )
    if result:
        Lead.objects.filter(pk=lead.pk).update(telegram_message_id=result["message_id"])


def refresh_lead_message(lead_id: int) -> None:
    from crm.models import Lead

    lead = Lead.objects.select_related("service", "assignee").filter(pk=lead_id).first()
    if not (lead and lead.telegram_message_id and settings.TELEGRAM_CHAT_ID):
        return
    call(
        "editMessageText",
        chat_id=settings.TELEGRAM_CHAT_ID,
        message_id=lead.telegram_message_id,
        text=lead_text(lead),
        parse_mode="HTML",
        reply_markup=lead_keyboard(lead),
        disable_web_page_preview=True,
    )


def notify_new_lead_async(lead_id: int) -> None:
    if enabled():
        run_async(notify_new_lead, lead_id)


def refresh_lead_message_async(lead_id: int) -> None:
    if enabled():
        run_async(refresh_lead_message, lead_id)


# --- Обработка входящих обновлений -----------------------------------------


def staff_by_telegram(tg_user: dict):
    from crm.models import StaffProfile

    profile = (
        StaffProfile.objects.select_related("user")
        .filter(telegram_id=tg_user.get("id"), user__is_active=True, user__is_staff=True)
        .first()
    )
    return profile.user if profile else None


def reply(chat_id: int, text: str) -> None:
    call("sendMessage", chat_id=chat_id, text=text, parse_mode="HTML", disable_web_page_preview=True)


def handle_update(update: dict) -> None:
    if "callback_query" in update:
        handle_callback(update["callback_query"])
    elif "message" in update:
        handle_message(update["message"])


def handle_message(message: dict) -> None:
    from crm.models import OPEN_STATUSES, Lead, StaffProfile

    text = (message.get("text") or "").strip()
    chat_id = message["chat"]["id"]
    tg_user = message.get("from") or {}
    if not text.startswith("/"):
        return
    command, _, arg = text.partition(" ")
    command = command.split("@")[0].lower()

    if command == "/start":
        reply(
            chat_id,
            "Это рабочий бот CRM. Чтобы получать доступ к заявкам, отправьте "
            "<code>/link КОД</code> — код есть в вашем профиле сотрудника в CRM.\n"
            f"ID этого чата: <code>{chat_id}</code>",
        )
        return

    if command == "/link":
        profile = StaffProfile.objects.select_related("user").filter(link_code=arg.strip().upper()).first()
        if not profile or not profile.user.is_active:
            reply(chat_id, "Код не найден. Проверьте его в профиле сотрудника в CRM.")
            return
        StaffProfile.objects.filter(telegram_id=tg_user.get("id")).exclude(pk=profile.pk).update(telegram_id=None)
        profile.telegram_id = tg_user.get("id")
        profile.telegram_username = tg_user.get("username", "")
        profile.save(update_fields=["telegram_id", "telegram_username"])
        reply(chat_id, f"Готово, {html.escape(profile.user.get_full_name() or profile.user.username)}! Telegram привязан.")
        return

    user = staff_by_telegram(tg_user)
    if not user:
        reply(chat_id, "Нет доступа. Привяжите аккаунт командой /link КОД.")
        return

    if command in {"/today", "/my"}:
        leads = Lead.objects.filter(assignee=user, status__in=OPEN_STATUSES).select_related("service")[:20]
        title = "Ваши открытые заявки"
    elif command == "/new":
        leads = Lead.objects.filter(status="new", assignee__isnull=True).select_related("service")[:20]
        title = "Новые заявки без ответственного"
    else:
        reply(chat_id, "Команды: /new — новые заявки, /today — мои открытые заявки.")
        return

    if not leads:
        reply(chat_id, f"{title}: нет.")
        return
    rows = [
        f"#{lead.pk} · {html.escape(lead.get_status_display())} · {html.escape(lead.name or '—')} · "
        f"<code>{html.escape(lead.phone)}</code>" + (f" · {html.escape(lead.service.title)}" if lead.service else "")
        for lead in leads
    ]
    reply(chat_id, f"<b>{title}</b>\n" + "\n".join(rows))


def handle_callback(query: dict) -> None:
    from crm.models import Lead, LeadStatus

    data = query.get("data") or ""
    user = staff_by_telegram(query.get("from") or {})
    if not user:
        call("answerCallbackQuery", callback_query_id=query["id"], text="Нет доступа: привяжите аккаунт /link", show_alert=True)
        return

    parts = data.split(":")
    if len(parts) < 3 or parts[0] != "lead" or not parts[1].isdigit():
        call("answerCallbackQuery", callback_query_id=query["id"])
        return
    lead = Lead.objects.select_related("service", "assignee").filter(pk=int(parts[1])).first()
    if not lead:
        call("answerCallbackQuery", callback_query_id=query["id"], text="Заявка не найдена")
        return

    action = parts[2]
    if action == "take":
        lead.assignee = user
        if lead.status == LeadStatus.NEW:
            lead.status = LeadStatus.IN_WORK
        notice = "Заявка ваша"
    elif action == "status" and len(parts) == 4 and parts[3] in LeadStatus.values:
        lead.status = parts[3]
        if not lead.assignee_id:
            lead.assignee = user
        notice = f"Этап: {lead.get_status_display()}"
    else:
        call("answerCallbackQuery", callback_query_id=query["id"])
        return

    lead.save(actor=user)  # история пишется в save(), карточка обновится после коммита
    call("answerCallbackQuery", callback_query_id=query["id"], text=notice)
    message = query.get("message") or {}
    if message and lead.telegram_message_id != message.get("message_id"):
        # Карточка в другом чате (например, в личке) — обновим её тоже.
        call(
            "editMessageText",
            chat_id=message["chat"]["id"],
            message_id=message["message_id"],
            text=lead_text(lead),
            parse_mode="HTML",
            reply_markup=lead_keyboard(lead),
        )
