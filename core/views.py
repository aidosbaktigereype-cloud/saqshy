from django.conf import settings
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext as _

from cases.models import Case
from core import seo
from core.models import Page
from services.models import FAQ, Package, Service


def home(request):
    services = Service.objects.filter(is_active=True).prefetch_related(
        Prefetch("packages", queryset=Package.objects.order_by("order"))
    )
    context = {
        "services": services,
        "cases": Case.objects.filter(is_published=True).prefetch_related("services")[:6],
        "faqs": FAQ.objects.filter(service__isnull=True),
        "seo": {
            "title": _("Установка охранных систем AJAX, видеонаблюдения и СКУД в Алматы"),
            "description": _(
                "Монтаж сигнализации AJAX, камер видеонаблюдения, СКУД и слаботочных сетей в Алматы под ключ. "
                "Бесплатный выезд и смета, гарантия на работы."
            ),
        },
    }
    context["jsonld"] = [seo.local_business(), seo.faq_page(context["faqs"])]
    return render(request, "core/home.html", context)


def page(request, slug):
    obj = get_object_or_404(Page, slug=slug)
    context = {
        "page": obj,
        "seo": {"title": obj.seo_title or obj.title, "description": obj.seo_description or obj.lead[:160]},
        "jsonld": [seo.breadcrumbs([(_("Главная"), reverse("home")), (obj.title, request.path)])],
    }
    return render(request, "core/page.html", context)


def contacts(request):
    context = {
        "seo": {
            "title": _("Контакты — установка охранных систем в Алматы"),
            "description": _("Телефон, WhatsApp, Telegram и адрес. Выезд мастера по Алматы и пригородам."),
        },
        "jsonld": [seo.local_business(), seo.breadcrumbs([(_("Главная"), reverse("home")), (_("Контакты"), request.path)])],
    }
    return render(request, "core/contacts.html", context)


def thanks(request):
    return render(request, "core/thanks.html", {"seo": {"title": _("Заявка отправлена"), "noindex": True}})


def not_found(request, exception=None):
    return render(request, "core/404.html", {"seo": {"title": _("Страница не найдена"), "noindex": True}}, status=404)


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /crm/",
        "Disallow: /api/",
        "Disallow: /spasibo/",
        "Disallow: /kk/spasibo/",
        "Disallow: /en/spasibo/",
        f"Sitemap: {settings.SITE_URL}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")


def healthz(request):
    return HttpResponse("ok", content_type="text/plain")
