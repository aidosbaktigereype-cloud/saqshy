"""Тесты канбана, сводки, 2FA, WhatsApp и напоминаний."""

import hashlib
import hmac
import json
from datetime import timedelta
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.utils import timezone

from crm import telegram, whatsapp
from crm.models import Lead, Message, StaffProfile
from crm.reminders import send_due


@override_settings(ADMIN_2FA_REQUIRED=False)
class BoardAndDashboardTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser("boss", "boss@example.kz", "x" * 12)
        self.client.force_login(self.admin)

    def test_move_card_changes_status_and_assigns(self):
        lead = Lead.objects.create(phone="+7 701 333 33 33")
        response = self.client.post(f"/crm/crm/lead/{lead.pk}/move/", {"status": "measure"})
        self.assertEqual(response.json(), {"ok": True})
        lead.refresh_from_db()
        self.assertEqual((lead.status, lead.assignee), ("measure", self.admin))
        self.assertTrue(lead.events.filter(kind="status").exists())

    def test_move_rejects_unknown_status(self):
        lead = Lead.objects.create(phone="+7 701 333 33 33")
        self.assertEqual(self.client.post(f"/crm/crm/lead/{lead.pk}/move/", {"status": "x"}).status_code, 400)

    def test_dashboard_counts_and_admin_is_russian(self):
        Lead.objects.create(phone="+7 701 333 33 33")
        response = self.client.get("/crm/", HTTP_ACCEPT_LANGUAGE="en")
        self.assertContains(response, "Заявок сегодня")
        self.assertEqual(response.context["dash"]["today"], 1)
        self.assertContains(self.client.get("/crm/crm/lead/", HTTP_ACCEPT_LANGUAGE="en"), "Выберите")


class TwoFactorTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser("boss", "boss@example.kz", "x" * 12)
        self.client.force_login(self.admin)

    def test_superuser_without_device_must_set_up(self):
        self.assertRedirects(self.client.get("/crm/"), "/crm/2fa/setup/", fetch_redirect_response=False)
        self.assertContains(self.client.get("/crm/2fa/setup/"), "<svg")

    def test_setup_and_verify_flow(self):
        from django_otp.oath import totp
        from django_otp.plugins.otp_totp.models import TOTPDevice

        self.client.get("/crm/2fa/setup/")
        device = TOTPDevice.objects.get(user=self.admin)
        code = f"{totp(device.bin_key, device.step, device.t0, device.digits, device.drift):06d}"
        response = self.client.post("/crm/2fa/setup/", {"token": code})
        self.assertRedirects(response, "/crm/", fetch_redirect_response=False)
        self.assertEqual(self.client.get("/crm/").status_code, 200)

        other = self.client_class()
        other.force_login(self.admin)
        self.assertTrue(other.get("/crm/crm/lead/")["Location"].startswith("/crm/2fa/verify/"))
        self.assertContains(other.post("/crm/2fa/verify/", {"token": "000000"}), "Неверный")


def wa_payload(text="Здравствуйте, нужна сигнализация", msg_id="wamid.1", wa_id="77011234567"):
    value = {
        "contacts": [{"wa_id": wa_id, "profile": {"name": "Ерлан"}}],
        "messages": [{"from": wa_id, "id": msg_id, "type": "text", "text": {"body": text}}],
    }
    return {"entry": [{"changes": [{"value": value}]}]}


@override_settings(
    WHATSAPP_TOKEN="wa-token",
    WHATSAPP_PHONE_NUMBER_ID="123",
    WHATSAPP_VERIFY_TOKEN="verify-me",
    WHATSAPP_APP_SECRET="app-secret",
    TELEGRAM_BOT_TOKEN="",
    TELEGRAM_CHAT_ID="-100",
)
class WhatsAppTests(TestCase):
    def post(self, payload, secret="app-secret"):
        body = json.dumps(payload).encode()
        signature = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        return self.client.post(
            "/wa/webhook/", data=body, content_type="application/json", HTTP_X_HUB_SIGNATURE_256=signature
        )

    def test_verification_handshake(self):
        params = {"hub.mode": "subscribe", "hub.verify_token": "verify-me", "hub.challenge": "42"}
        self.assertEqual(self.client.get("/wa/webhook/", params).content, b"42")
        params["hub.verify_token"] = "nope"
        self.assertEqual(self.client.get("/wa/webhook/", params).status_code, 403)

    def test_rejects_bad_signature(self):
        self.assertEqual(self.post(wa_payload(), secret="wrong").status_code, 403)
        self.assertFalse(Lead.objects.exists())

    def test_incoming_message_creates_lead_and_dedupes(self):
        self.post(wa_payload())
        self.post(wa_payload())  # Meta повторила то же сообщение
        self.post(wa_payload(text="Квартира, 3 комнаты", msg_id="wamid.2"))
        lead = Lead.objects.get()
        self.assertEqual((lead.phone, lead.name, lead.source), ("+7 701 123 45 67", "Ерлан", "messenger"))
        self.assertEqual(lead.messages.count(), 2)

    def test_reply_from_telegram_group(self):
        self.post(wa_payload())
        lead = Lead.objects.get()
        Lead.objects.filter(pk=lead.pk).update(telegram_message_id=555)
        user = get_user_model().objects.create_user("ops", password="x" * 12, is_staff=True)
        StaffProfile.objects.filter(user=user).update(telegram_id=777)
        update = {
            "message": {
                "message_id": 10,
                "text": "Добрый день! Когда удобно приехать?",
                "chat": {"id": -100},
                "from": {"id": 777},
                "reply_to_message": {"message_id": 555, "from": {"is_bot": True}},
            }
        }
        with override_settings(TELEGRAM_BOT_TOKEN="t"), mock.patch.object(
            telegram, "call", return_value={"message_id": 1}
        ), mock.patch("crm.whatsapp.send_text", return_value="wamid.out") as send:
            telegram.handle_update(update)
        send.assert_called_once_with("77011234567", "Добрый день! Когда удобно приехать?")
        self.assertTrue(Message.objects.filter(lead=lead, direction="out", author=user).exists())

    def test_reply_blocked_after_24h(self):
        self.post(wa_payload())
        Message.objects.update(created_at=timezone.now() - timedelta(hours=25))
        ok, info = whatsapp.reply(Lead.objects.get(), "Привет")
        self.assertFalse(ok)
        self.assertIn("24", info)


@override_settings(TELEGRAM_BOT_TOKEN="t", TELEGRAM_CHAT_ID="-100")
class ReminderTests(TestCase):
    def test_due_reminder_sent_once_to_assignee(self):
        user = get_user_model().objects.create_user("ops", password="x" * 12, is_staff=True)
        StaffProfile.objects.filter(user=user).update(telegram_id=777)
        lead = Lead.objects.create(
            phone="+7 701 444 44 44", assignee=user, status="in_work", next_action_at=timezone.now() - timedelta(minutes=1)
        )
        Lead.objects.create(phone="+7 701 555 55 55", next_action_at=timezone.now() + timedelta(hours=1))
        with mock.patch.object(telegram, "call", return_value={"message_id": 1}) as call:
            self.assertEqual(send_due(), 1)
            self.assertEqual(send_due(), 0)
        self.assertEqual(call.call_args.kwargs["chat_id"], 777)
        lead.refresh_from_db()
        self.assertIsNotNone(lead.reminder_sent_at)
