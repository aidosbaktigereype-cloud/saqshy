from urllib.parse import quote

from django.conf import settings
from django.urls import translate_url
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.translation import gettext as _

from services.models import Service


def site(request):
    lang = get_language() or settings.LANGUAGE_CODE
    brand = settings.BRAND
    wa_text = _("Здравствуйте! Хочу узнать стоимость установки охранной системы.")
    path = request.path
    languages = [
        {"code": code, "name": name, "url": translate_url(path, code), "active": code == lang}
        for code, name in settings.LANGUAGES
    ]
    return {
        "BRAND": brand,
        "FEATURES": settings.FEATURES,
        "ANALYTICS": settings.ANALYTICS,
        "SITE_URL": settings.SITE_URL,
        "LANG": lang,
        "LANGUAGES_NAV": languages,
        "CANONICAL": settings.SITE_URL + path,
        "PHONE_HREF": "tel:+" + "".join(ch for ch in brand["phone"] if ch.isdigit()),
        "WHATSAPP_URL": f"https://wa.me/{brand['whatsapp']}?text={quote(wa_text)}",
        "TELEGRAM_URL": f"https://t.me/{brand['telegram']}",
        "NAV_SERVICES": Service.objects.filter(is_active=True).only("slug", "title", "icon"),
        "YEAR": timezone.now().year,
    }
