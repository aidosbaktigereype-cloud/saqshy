from modeltranslation.translator import TranslationOptions, register

from core.models import Page


@register(Page)
class PageTR(TranslationOptions):
    fields = ("title", "lead", "body", "seo_title", "seo_description")
