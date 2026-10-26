from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

ROLES = {
    "Менеджер": {
        "crm.lead": ["view", "add", "change"],
        "crm.leadevent": ["view"],
        "services.service": ["view"],
        "services.package": ["view"],
        "cases.case": ["view"],
    },
    "Контент-менеджер": {
        "services.service": ["view", "add", "change"],
        "services.package": ["view", "add", "change", "delete"],
        "services.faq": ["view", "add", "change", "delete"],
        "cases.case": ["view", "add", "change", "delete"],
        "core.page": ["view", "add", "change"],
        "crm.lead": ["view"],
    },
}


class Command(BaseCommand):
    help = "Создаёт роли сотрудников (группы с правами). Полный доступ — у суперпользователей."

    def handle(self, *args, **options):
        for name, models in ROLES.items():
            group, _ = Group.objects.get_or_create(name=name)
            perms = []
            for model_label, actions in models.items():
                app_label, model = model_label.split(".")
                for action in actions:
                    perms.append(Permission.objects.get(content_type__app_label=app_label, codename=f"{action}_{model}"))
            group.permissions.set(perms)
            self.stdout.write(self.style.SUCCESS(f"Роль «{name}»: {len(perms)} прав"))
        self.stdout.write("Сотруднику с ролью нужно включить «Статус персонала» (is_staff), чтобы войти в CRM.")
