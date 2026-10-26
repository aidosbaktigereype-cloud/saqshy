"""Настройки проекта. Всё, что отличается между окружениями, читается из .env."""

import os
from pathlib import Path

import dj_database_url
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def env_bool(name: str, default: bool = False) -> bool:
    return env(name, "1" if default else "0").lower() in {"1", "true", "yes", "on"}


def env_list(name: str, default: str = "") -> list[str]:
    return [item.strip() for item in env(name, default).split(",") if item.strip()]


DEBUG = env_bool("DJANGO_DEBUG", False)
SECRET_KEY = env("DJANGO_SECRET_KEY") or ("dev-insecure-key" if DEBUG else "")
if not SECRET_KEY:
    raise RuntimeError("DJANGO_SECRET_KEY is required when DJANGO_DEBUG is off")

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")
SITE_URL = env("SITE_URL", "http://127.0.0.1:8000").rstrip("/")

INSTALLED_APPS = [
    "modeltranslation",  # должен стоять до django.contrib.admin
    "unfold",
    "unfold.contrib.filters",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "core",
    "services",
    "cases",
    "crm",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# SQLite по умолчанию для локальной разработки, PostgreSQL — через DATABASE_URL.
DATABASES = {
    "default": dj_database_url.parse(
        env("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=60,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Языки ---------------------------------------------------------------
LANGUAGE_CODE = "ru"
LANGUAGES = [
    ("ru", "Русский"),
    ("kk", "Қазақша"),
    ("en", "English"),
]
LOCALE_PATHS = [BASE_DIR / "locale"]
USE_I18N = True
TIME_ZONE = "Asia/Almaty"
USE_TZ = True

MODELTRANSLATION_DEFAULT_LANGUAGE = "ru"
MODELTRANSLATION_FALLBACK_LANGUAGES = ("ru",)

# --- Статика и медиа -----------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = Path(env("MEDIA_ROOT", str(BASE_DIR / "media")))
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        if DEBUG
        else "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

# --- Безопасность в продакшене ------------------------------------------
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = env_bool("DJANGO_SSL_REDIRECT", True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(env("DJANGO_HSTS_SECONDS", "3600"))
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# --- Почта ---------------------------------------------------------------
EMAIL_BACKEND = env("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = int(env("EMAIL_PORT", "587"))
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "noreply@localhost")
LEAD_NOTIFY_EMAILS = env_list("LEAD_NOTIFY_EMAILS")

# --- Бренд и контакты (подтягиваются из конфига) -------------------------
BRAND = {
    "name": env("BRAND_NAME", "Saqshy"),
    "phone": env("CONTACT_PHONE", "+7 700 000 00 00"),
    "whatsapp": env("CONTACT_WHATSAPP", "77000000000"),
    "telegram": env("CONTACT_TELEGRAM", "saqshy_kz"),
    "email": env("CONTACT_EMAIL", "info@example.kz"),
    "city": env("CONTACT_CITY", "Алматы"),
    "address": env("CONTACT_ADDRESS", "Алматы"),
    "hours": env("CONTACT_HOURS", "Пн–Сб 9:00–20:00"),
    "legal": env("LEGAL_INFO", ""),
    "instagram": env("CONTACT_INSTAGRAM", ""),
}

# Будущие модули: включаются флагами, когда будут готовы.
FEATURES = {
    "catalog": env_bool("FEATURE_CATALOG", False),
    "cart": env_bool("FEATURE_CART", False),
    "accounts": env_bool("FEATURE_ACCOUNTS", False),
    "quiz": env_bool("FEATURE_QUIZ", False),
}

# --- Аналитика и реклама -------------------------------------------------
ANALYTICS = {
    "ga4": env("GA4_ID"),
    "metrika": env("YANDEX_METRIKA_ID"),
    "gads": env("GOOGLE_ADS_ID"),
    "gads_lead_label": env("GOOGLE_ADS_LEAD_LABEL"),
}

# --- Telegram ------------------------------------------------------------
TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = env("TELEGRAM_CHAT_ID")
TELEGRAM_WEBHOOK_SECRET = env("TELEGRAM_WEBHOOK_SECRET")

# Антиспам для формы заявки: не больше N заявок с одного IP за окно (секунды).
LEAD_RATE_LIMIT = int(env("LEAD_RATE_LIMIT", "5"))
LEAD_RATE_WINDOW = int(env("LEAD_RATE_WINDOW", "600"))

# --- Админка / CRM -------------------------------------------------------
UNFOLD = {
    "SITE_TITLE": f"{BRAND['name']} CRM",
    "SITE_HEADER": f"{BRAND['name']} CRM",
    "SITE_SUBHEADER": "Заявки и контент",
    "SITE_URL": "/",
    "SITE_SYMBOL": "shield",
    "SHOW_VIEW_ON_SITE": True,
    "COLORS": {
        "primary": {
            "50": "oklch(97% .02 75)",
            "100": "oklch(94% .05 75)",
            "200": "oklch(89% .09 75)",
            "300": "oklch(84% .13 72)",
            "400": "oklch(79% .15 68)",
            "500": "oklch(74% .16 65)",
            "600": "oklch(66% .16 58)",
            "700": "oklch(56% .14 52)",
            "800": "oklch(46% .11 50)",
            "900": "oklch(38% .09 50)",
            "950": "oklch(27% .07 50)",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("CRM"),
                "items": [
                    {"title": _("Заявки"), "icon": "inbox", "link": "/crm/crm/lead/"},
                    {"title": _("Новые заявки"), "icon": "notifications", "link": "/crm/crm/lead/?status__exact=new"},
                    {"title": _("История"), "icon": "history", "link": "/crm/crm/leadevent/"},
                ],
            },
            {
                "title": _("Контент сайта"),
                "items": [
                    {"title": _("Услуги"), "icon": "construction", "link": "/crm/services/service/"},
                    {"title": _("Пакеты"), "icon": "sell", "link": "/crm/services/package/"},
                    {"title": _("Вопросы и ответы"), "icon": "quiz", "link": "/crm/services/faq/"},
                    {"title": _("Кейсы"), "icon": "photo_library", "link": "/crm/cases/case/"},
                    {"title": _("Страницы"), "icon": "article", "link": "/crm/core/page/"},
                ],
            },
            {
                "title": _("Доступы"),
                "items": [
                    {"title": _("Сотрудники"), "icon": "badge", "link": "/crm/auth/user/"},
                    {"title": _("Роли"), "icon": "group", "link": "/crm/auth/group/"},
                ],
            },
        ],
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": env("LOG_LEVEL", "INFO")},
}
