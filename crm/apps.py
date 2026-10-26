from django.apps import AppConfig


class CrmConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "crm"
    verbose_name = "CRM"

    def ready(self) -> None:
        from django.contrib.auth import get_user_model
        from django.db.models.signals import post_save

        from crm.models import StaffProfile

        def ensure_profile(sender, instance, created, **kwargs):
            if instance.is_staff:
                StaffProfile.objects.get_or_create(user=instance)

        post_save.connect(ensure_profile, sender=get_user_model(), dispatch_uid="crm_staff_profile")
