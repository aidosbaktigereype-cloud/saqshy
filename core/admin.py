from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from core.models import Page


@admin.register(Page)
class PageAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("title", "slug", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "lead", "body")}),
        ("SEO", {"fields": ("seo_title", "seo_description")}),
    )
