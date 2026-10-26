from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from cases.models import Case
from services.models import Service


class I18nSitemap(Sitemap):
    """Каждая страница на трёх языках + hreflang-альтернативы в sitemap.xml."""

    i18n = True
    alternates = True
    x_default = True


class StaticSitemap(I18nSitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return ["home", "case_list", "contacts", "about", "privacy"]

    def location(self, item):
        return reverse(item)


class ServiceSitemap(I18nSitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Service.objects.filter(is_active=True)


class CaseSitemap(I18nSitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return Case.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.created_at


SITEMAPS = {"static": StaticSitemap, "services": ServiceSitemap, "cases": CaseSitemap}
