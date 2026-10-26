from modeltranslation.translator import TranslationOptions, register

from cases.models import Case


@register(Case)
class CaseTR(TranslationOptions):
    fields = ("title", "object_type", "district", "task", "solution", "equipment", "duration")
