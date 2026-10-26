from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline
from unfold.admin import ModelAdmin, StackedInline

from services.models import FAQ, Package, Service


class PackageInline(StackedInline, TranslationStackedInline):
    model = Package
    extra = 0
    fields = ("name", "items", ("price_from", "price_note"), ("is_popular", "order"))


class FAQInline(StackedInline, TranslationStackedInline):
    model = FAQ
    extra = 0
    fields = ("question", "answer", "order")


@admin.register(Service)
class ServiceAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("title", "slug", "price_from", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("title_ru",)}
    inlines = [PackageInline, FAQInline]
    fieldsets = (
        (None, {"fields": ("title", "slug", "icon", ("price_from", "order", "is_active"))}),
        ("Страница", {"fields": ("h1", "offer", "summary", "intro", "benefits", "object_types")}),
        ("SEO", {"fields": ("seo_title", "seo_description")}),
    )


@admin.register(Package)
class PackageAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("name", "service", "price_from", "is_popular", "order")
    list_filter = ("service",)
    list_editable = ("price_from", "is_popular", "order")


@admin.register(FAQ)
class FAQAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("question", "service", "order")
    list_filter = ("service",)
    list_editable = ("order",)
    search_fields = ("question", "answer")
