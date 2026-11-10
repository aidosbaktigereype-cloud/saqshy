"""KUZET в текстах (не в названии бренда KUZET BM): ru — КУЗЕТ, kk — КҮЗЕТ, en — KUZET (Security)."""

import re

from django.db import migrations

TOKEN = re.compile(r"KUZET(?! BM)(?! \(Security\))")
BY_LANG = {"ru": "КУЗЕТ", "kk": "КҮЗЕТ", "en": "KUZET (Security)"}

MODELS = [
    ("core", "Page"),
    ("services", "Service"),
    ("services", "Package"),
    ("services", "FAQ"),
    ("cases", "Case"),
]


def replacement_for(field_name: str) -> str:
    for lang, repl in BY_LANG.items():
        if field_name.endswith(f"_{lang}"):
            return repl
    return BY_LANG["ru"]  # основное поле хранит русский текст


def forwards(apps, schema_editor):
    for app_label, model_name in MODELS:
        model = apps.get_model(app_label, model_name)
        fields = [f.name for f in model._meta.fields if f.get_internal_type() in ("CharField", "TextField")]
        for obj in model.objects.all():
            changed = []
            for name in fields:
                value = getattr(obj, name)
                if value and TOKEN.search(value):
                    setattr(obj, name, TOKEN.sub(replacement_for(name), value))
                    changed.append(name)
            if changed:
                obj.save(update_fields=changed)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_rebrand_kuzet_bm"),
        ("services", "0003_service_icon_kuzet_label"),
        ("cases", "0001_initial"),
    ]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
