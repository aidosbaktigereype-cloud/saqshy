from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext as _

from cases.models import Case
from core import seo
from services.models import Service


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    faqs = list(service.faqs.all())
    context = {
        "service": service,
        "packages": service.packages.all(),
        "faqs": faqs,
        "cases": Case.objects.filter(is_published=True, services=service)[:3],
        "other_services": Service.objects.filter(is_active=True).exclude(pk=service.pk),
        "seo": {
            "title": service.seo_title or service.h1,
            "description": service.seo_description or service.summary,
        },
        "jsonld": [
            seo.service(service),
            seo.faq_page(faqs),
            seo.breadcrumbs([(_("Главная"), reverse("home")), (service.title, request.path)]),
        ],
    }
    return render(request, "services/detail.html", context)
