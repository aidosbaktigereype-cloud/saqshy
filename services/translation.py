from modeltranslation.translator import TranslationOptions, register

from services.models import FAQ, Package, Service


@register(Service)
class ServiceTR(TranslationOptions):
    fields = ("title", "h1", "offer", "summary", "intro", "benefits", "object_types", "seo_title", "seo_description")


@register(Package)
class PackageTR(TranslationOptions):
    fields = ("name", "items", "price_note")


@register(FAQ)
class FAQTR(TranslationOptions):
    fields = ("question", "answer")
