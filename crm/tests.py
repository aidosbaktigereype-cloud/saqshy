import json
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase, override_settings

from crm import telegram
from crm.models import Lead, LeadEvent, LeadStatus, StaffProfile
from crm.views import normalize_phone


def post_lead(client, **overrides):
    data = {"name": "Айгерим", "phone": "8 701 234-56-78", "consent": "1", "service": "ajax", "locale": "kk"}
    data.update(overrides)
    return client.post("/api/leads/", data=json.dumps(data), content_type="application/json", HTTP_ACCEPT="application/json")


class LeadApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", verbosity=0)

    def setUp(self):
        cache.clear()

    def test_phone_normalization(self):
        self.assertEqual(normalize_phone("8 (701) 234-56-78"), "+7 701 234 56 78")
        self.assertEqual(normalize_phone("7012345678"), "+7 701 234 56 78")
        self.assertIsNone(normalize_phone("123"))

    def test_creates_lead_with_history(self):
        response = post_lead(self.client, utm_source="google", gclid="abc")
        self.assertEqual(response.json(), {"ok": True, "errors": {}})
        lead = Lead.objects.get()
        self.assertEqual(lead.phone, "+7 701 234 56 78")
        self.assertEqual(lead.service.slug, "ajax")
        self.assertEqual((lead.locale, lead.utm_source, lead.gclid), ("kk", "google", "abc"))
        self.assertEqual(lead.events.get().kind, LeadEvent.Kind.CREATED)

    def test_rejects_invalid_phone_and_missing_consent(self):
        response = post_lead(self.client, phone="12", consent="")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.json()["errors"]), {"phone", "consent"})
        self.assertFalse(Lead.objects.exists())

    def test_honeypot_silently_drops_bots(self):
        response = post_lead(self.client, website="http://spam")
        self.assertTrue(response.json()["ok"])
        self.assertFalse(Lead.objects.exists())

    @override_settings(LEAD_RATE_LIMIT=2)
    def test_rate_limit(self):
        self.assertEqual(post_lead(self.client).status_code, 200)
        self.assertEqual(post_lead(self.client).status_code, 200)
        self.assertEqual(post_lead(self.client).status_code, 429)

    def test_plain_form_post_redirects_to_localized_thanks(self):
        response = self.client.post("/api/leads/", {"phone": "+77012345678", "consent": "on", "locale": "en"})
        self.assertRedirects(response, "/en/spasibo/")


class LeadWorkflowTests(TestCase):
    def setUp(self):
        self.manager = get_user_model().objects.create_user("manager", password="x" * 12, is_staff=True)

    def test_status_and_assignee_changes_are_logged(self):
        lead = Lead.objects.create(phone="+7 701 000 00 00")
        lead = Lead.objects.get(pk=lead.pk)
        lead.status = LeadStatus.MEASURE
        lead.assignee = self.manager
        lead.save(actor=self.manager)
        kinds = list(lead.events.order_by("id").values_list("kind", flat=True))
        self.assertEqual(kinds, ["created", "status", "assign"])
        self.assertEqual(lead.events.get(kind="status").text, "Новая → Замер назначен")

    def test_staff_profile_created_with_link_code(self):
        self.assertTrue(StaffProfile.objects.get(user=self.manager).link_code)


@override_settings(TELEGRAM_BOT_TOKEN="test-token", TELEGRAM_CHAT_ID="-100", TELEGRAM_WEBHOOK_SECRET="s3cret")
class TelegramTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("ops", password="x" * 12, is_staff=True)
        self.profile = self.user.staff_profile

    def webhook(self, update, secret="s3cret"):
        return self.client.post(
            "/tg/webhook/", data=json.dumps(update), content_type="application/json",
            HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN=secret,
        )

    def test_webhook_requires_secret(self):
        self.assertEqual(self.webhook({}, secret="wrong").status_code, 403)

    @mock.patch.object(telegram, "call", return_value={"message_id": 1})
    def test_link_and_take_lead(self, call):
        self.webhook({"message": {"text": f"/link {self.profile.link_code}", "chat": {"id": 5}, "from": {"id": 777, "username": "ops"}}})
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.telegram_id, 777)

        lead = Lead.objects.create(phone="+7 701 111 11 11")
        self.webhook({"callback_query": {"id": "q1", "data": f"lead:{lead.pk}:take", "from": {"id": 777}, "message": {"message_id": 1, "chat": {"id": -100}}}})
        lead.refresh_from_db()
        self.assertEqual(lead.assignee, self.user)
        self.assertEqual(lead.status, LeadStatus.IN_WORK)

    @mock.patch.object(telegram, "call", return_value=None)
    def test_unlinked_user_cannot_change_leads(self, call):
        lead = Lead.objects.create(phone="+7 701 111 11 11")
        self.webhook({"callback_query": {"id": "q1", "data": f"lead:{lead.pk}:status:done", "from": {"id": 999}}})
        lead.refresh_from_db()
        self.assertEqual(lead.status, LeadStatus.NEW)

    def test_lead_card_text(self):
        lead = Lead.objects.create(name="<b>", phone="+7 701 111 11 11")
        text = telegram.lead_text(lead)
        self.assertIn("&lt;b&gt;", text)
        self.assertIn("Заявка #", text)


@override_settings(ADMIN_2FA_REQUIRED=False)
class AdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", verbosity=0)

    def setUp(self):
        self.admin = get_user_model().objects.create_superuser("boss", "boss@example.kz", "x" * 12)
        self.client.force_login(self.admin)

    def test_crm_pages_render(self):
        lead = Lead.objects.create(phone="+7 701 222 22 22")
        for url in [
            "/crm/", "/crm/crm/lead/", f"/crm/crm/lead/{lead.pk}/change/", "/crm/crm/lead/add/",
            "/crm/services/service/", "/crm/services/service/1/change/", "/crm/cases/case/", "/crm/core/page/",
            "/crm/auth/user/", f"/crm/auth/user/{self.admin.pk}/change/", "/crm/crm/lead/board/",
            "/crm/crm/message/", "/crm/2fa/setup/",
        ]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_comment_from_admin_goes_to_history(self):
        lead = Lead.objects.create(phone="+7 701 222 22 22")
        response = self.client.post(
            f"/crm/crm/lead/{lead.pk}/change/",
            {
                "name": "", "phone": lead.phone, "source": "form", "status": "in_work", "assignee": self.admin.pk,
                "new_comment": "Перезвонить вечером",
                "events-TOTAL_FORMS": "1", "events-INITIAL_FORMS": "1", "events-MIN_NUM_FORMS": "0", "events-MAX_NUM_FORMS": "1000",
                "events-0-id": lead.events.get().pk, "events-0-lead": lead.pk,
                "messages-TOTAL_FORMS": "0", "messages-INITIAL_FORMS": "0",
                "messages-MIN_NUM_FORMS": "0", "messages-MAX_NUM_FORMS": "1000",
            },
        )
        self.assertEqual(response.status_code, 302, response.content[:2000])
        self.assertTrue(lead.events.filter(kind="comment", text="Перезвонить вечером", author=self.admin).exists())
        self.assertTrue(lead.events.filter(kind="status").exists())
