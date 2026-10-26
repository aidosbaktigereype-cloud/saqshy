from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext as _

from cases.models import Case
from core import seo


def case_list(request):
    context = {
        "cases": Case.objects.filter(is_published=True).prefetch_related("services"),
        "seo": {
            "title": _("Наши работы — кейсы по установке охранных систем в Алматы"),
            "description": _("Примеры объектов: квартиры, дома, офисы, магазины и склады. Состав, сроки и стоимость."),
        },
        "jsonld": [seo.breadcrumbs([(_("Главная"), reverse("home")), (_("Кейсы"), request.path)])],
    }
    return render(request, "cases/list.html", context)


def case_detail(request, slug):
    case = get_object_or_404(Case, slug=slug, is_published=True)
    context = {
        "case": case,
        "more_cases": Case.objects.filter(is_published=True).exclude(pk=case.pk)[:3],
        "seo": {"title": case.title, "description": case.task[:160]},
        "jsonld": [
            seo.breadcrumbs(
                [(_("Главная"), reverse("home")), (_("Кейсы"), reverse("case_list")), (case.title, request.path)]
            )
        ],
    }
    return render(request, "cases/detail.html", context)
