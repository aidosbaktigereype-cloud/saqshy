from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from cases.models import Case
from core import demo_data
from core.models import Page
from services.models import FAQ, Package, Service

LANGS = [code for code, _ in settings.LANGUAGES]


def set_translated(obj, field: str, values: dict) -> None:
    """Записывает значение поля на всех языках (title_ru, title_kk, title_en)."""
    for lang in LANGS:
        setattr(obj, f"{field}_{lang}", values.get(lang, ""))
    setattr(obj, field, values.get("ru", ""))


class Command(BaseCommand):
    help = "Наполняет сайт демо-контентом на трёх языках. Существующие записи не трогает без --force."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Перезаписать существующие услуги, кейсы и страницы")

    @transaction.atomic
    def handle(self, *args, force: bool = False, **options):
        created = {"services": 0, "cases": 0, "pages": 0}

        for order, data in enumerate(demo_data.SERVICES, start=1):
            service, is_new = Service.objects.get_or_create(slug=data["slug"], defaults={"title": data["title"]["ru"]})
            if not (is_new or force):
                continue
            created["services"] += 1
            service.icon = data["icon"]
            service.order = data.get("order", order)
            service.price_from = data["price_from"]
            service.is_active = True
            for field in ("title", "h1", "offer", "summary", "intro", "benefits", "object_types", "seo_title", "seo_description"):
                set_translated(service, field, data[field])
            service.save()

            service.packages.all().delete()
            for i, pkg in enumerate(data["packages"], start=1):
                package = Package(service=service, order=i, price_from=pkg["price_from"], is_popular=pkg.get("is_popular", False))
                set_translated(package, "name", pkg["name"])
                set_translated(package, "items", pkg["items"])
                set_translated(package, "price_note", pkg.get("price_note", {}))
                package.save()

            service.faqs.all().delete()
            for i, (question, answer) in enumerate(data["faqs"], start=1):
                faq = FAQ(service=service, order=i)
                set_translated(faq, "question", question)
                set_translated(faq, "answer", answer)
                faq.save()

        if force or not FAQ.objects.filter(service__isnull=True).exists():
            FAQ.objects.filter(service__isnull=True).delete()
            for i, (question, answer) in enumerate(demo_data.GENERAL_FAQS, start=1):
                faq = FAQ(order=i)
                set_translated(faq, "question", question)
                set_translated(faq, "answer", answer)
                faq.save()

        services_by_slug = {s.slug: s for s in Service.objects.all()}
        for data in demo_data.CASES:
            case, is_new = Case.objects.get_or_create(
                slug=data["slug"], defaults={"title": data["title"]["ru"], "task": "", "solution": ""}
            )
            if not (is_new or force):
                continue
            created["cases"] += 1
            case.amount = data["amount"]
            case.order = data["order"]
            case.is_demo = True
            case.is_published = True
            for field in ("title", "object_type", "district", "duration", "task", "solution", "equipment"):
                set_translated(case, field, data[field])
            case.save()
            case.services.set([services_by_slug[s] for s in data["services"] if s in services_by_slug])

        for data in demo_data.pages(settings.BRAND["name"]):
            page, is_new = Page.objects.get_or_create(slug=data["slug"], defaults={"title": data["title"]["ru"]})
            if not (is_new or force):
                continue
            created["pages"] += 1
            for field in ("title", "lead", "body"):
                set_translated(page, field, data[field])
            page.save()

        if options.get("verbosity", 1):
            self.stdout.write(self.style.SUCCESS(f"Готово: {created}"))
