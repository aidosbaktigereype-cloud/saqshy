from django.core.management import call_command
from django.test import TestCase, override_settings


class PublicPagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", verbosity=0)

    def test_pages_render_in_all_languages(self):
        paths = ["/", "/ajax/", "/keysy/", "/keysy/kvartira-bostandykskiy/", "/kontakty/", "/o-kompanii/", "/privacy/"]
        for prefix in ("", "/kk", "/en"):
            for path in paths:
                with self.subTest(url=prefix + path):
                    response = self.client.get(prefix + path)
                    self.assertEqual(response.status_code, 200)

    def test_language_is_applied(self):
        self.assertContains(self.client.get("/kk/ajax/"), "Алматыда AJAX дабылын орнату")
        self.assertContains(self.client.get("/en/ajax/"), "AJAX alarm installation in Almaty")
        self.assertContains(self.client.get("/ajax/"), "Установка сигнализации AJAX в Алматы")

    @override_settings(SITE_URL="https://example.kz")
    def test_seo_tags(self):
        html = self.client.get("/ajax/").content.decode()
        self.assertIn('<link rel="canonical" href="https://example.kz/ajax/"', html)
        self.assertIn('hreflang="kk" href="https://example.kz/kk/ajax/"', html)
        self.assertIn('hreflang="x-default"', html)
        self.assertIn('"@type": "FAQPage"', html)
        self.assertIn('"@type": "Service"', html)

    def test_thanks_page_is_noindex(self):
        self.assertContains(self.client.get("/spasibo/"), 'name="robots" content="noindex')

    def test_unknown_page_returns_404(self):
        self.assertEqual(self.client.get("/no-such-page/").status_code, 404)

    def test_sitemap_has_all_languages(self):
        xml = self.client.get("/sitemap.xml").content.decode()
        self.assertIn("/kk/videonablyudenie/", xml)
        self.assertIn("/en/skud/", xml)
        self.assertIn('hreflang="x-default"', xml)

    def test_robots_closes_crm(self):
        body = self.client.get("/robots.txt").content.decode()
        self.assertIn("Disallow: /crm/", body)
        self.assertIn("Sitemap:", body)
