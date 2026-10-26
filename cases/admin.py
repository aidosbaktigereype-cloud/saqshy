from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin
from unfold.decorators import display

from cases.models import Case


@admin.register(Case)
class CaseAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("title", "object_type", "district", "amount", "demo", "is_published", "order")
    list_filter = ("is_demo", "is_published", "services")
    list_editable = ("is_published", "order")
    search_fields = ("title", "task", "solution")
    filter_horizontal = ("services",)
    prepopulated_fields = {"slug": ("title_ru",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "image", ("is_published", "is_demo", "order"))}),
        ("Объект", {"fields": ("object_type", "district", "services")}),
        ("Описание", {"fields": ("task", "solution", "equipment", ("duration", "amount"))}),
    )

    @display(description="Демо", label={True: "warning", False: "success"})
    def demo(self, obj):
        return obj.is_demo, "демо" if obj.is_demo else "реальный"
