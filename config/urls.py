from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from cases import views as cases_views
from core import views as core_views
from core.sitemaps import SITEMAPS
from crm import twofa
from crm import views as crm_views
from services import views as services_views

urlpatterns = [
    path("crm/2fa/setup/", twofa.setup, name="twofa_setup"),
    path("crm/2fa/verify/", twofa.verify, name="twofa_verify"),
    path("crm/", admin.site.urls),
    path("wa/webhook/", crm_views.whatsapp_webhook, name="whatsapp_webhook"),
    path("api/leads/", crm_views.lead_create, name="lead_create"),
    path("tg/webhook/", crm_views.telegram_webhook, name="telegram_webhook"),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", core_views.robots_txt, name="robots_txt"),
    path("healthz/", core_views.healthz, name="healthz"),
]

# Публичные страницы: русский без префикса, /kk/ и /en/ — с префиксом.
urlpatterns += i18n_patterns(
    path("", core_views.home, name="home"),
    path("spasibo/", core_views.thanks, name="thanks"),
    path("keysy/", cases_views.case_list, name="case_list"),
    path("keysy/<slug:slug>/", cases_views.case_detail, name="case_detail"),
    path("kontakty/", core_views.contacts, name="contacts"),
    path("o-kompanii/", core_views.page, {"slug": "o-kompanii"}, name="about"),
    path("privacy/", core_views.page, {"slug": "privacy"}, name="privacy"),
    # Зарезервировано под будущие модули: /catalog/, /cart/, /checkout/, /account/.
    path("<slug:slug>/", services_views.service_detail, name="service_detail"),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "core.views.not_found"
