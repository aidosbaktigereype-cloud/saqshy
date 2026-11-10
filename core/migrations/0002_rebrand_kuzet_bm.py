"""Обновляет уже сохранённый контент: название бренда и формулировку «и т.д.» → «и другие»."""

from django.db import migrations

REPLACEMENTS = [
    ("Kuzet BAM", "KUZET BM"),
    ("Ajax, RAPTOR, STEMAX, Dahua и т.д.", "Ajax, RAPTOR, STEMAX, Dahua и другие"),
    ("Ajax, RAPTOR, STEMAX, Dahua және т.б. дабылдары", "Ajax, RAPTOR, STEMAX, Dahua және басқа дабылдар"),
]

MODELS = [
    ("core", "Page"),
    ("services", "Service"),
    ("services", "Package"),
    ("services", "FAQ"),
    ("cases", "Case"),
]


def forwards(apps, schema_editor):
    for app_label, model_name in MODELS:
        model = apps.get_model(app_label, model_name)
        text_fields = [f.name for f in model._meta.fields if f.get_internal_type() in ("CharField", "TextField")]
        for obj in model.objects.all():
            changed = []
            for name in text_fields:
                value = getattr(obj, name)
                if not value:
                    continue
                new = value
                for old, repl in REPLACEMENTS:
                    new = new.replace(old, repl)
                if new != value:
                    setattr(obj, name, new)
                    changed.append(name)
            if changed:
                obj.save(update_fields=changed)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
        ("services", "0002_alter_service_icon"),
        ("cases", "0001_initial"),
    ]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
