from django.db import models
from django.urls import reverse

from services.models import Service, split_lines


class Case(models.Model):
    slug = models.SlugField("URL", unique=True)
    title = models.CharField("Заголовок", max_length=200)
    object_type = models.CharField("Тип объекта", max_length=120)
    district = models.CharField("Район", max_length=120, blank=True)
    services = models.ManyToManyField(Service, related_name="cases", blank=True, verbose_name="Услуги")
    task = models.TextField("Задача")
    solution = models.TextField("Что сделали")
    equipment = models.TextField("Оборудование (по одному на строку)", blank=True)
    duration = models.CharField("Срок", max_length=60, blank=True)
    amount = models.PositiveIntegerField("Сумма, ₸", null=True, blank=True)
    image = models.ImageField("Фото", upload_to="cases/", blank=True)
    is_demo = models.BooleanField("Демо-кейс", default=False, help_text="Демо-кейсы нужно заменить реальными перед запуском")
    is_published = models.BooleanField("Опубликован", default=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "кейс"
        verbose_name_plural = "кейсы"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("case_detail", kwargs={"slug": self.slug})

    @property
    def equipment_list(self) -> list[str]:
        return split_lines(self.equipment)

    @property
    def main_service(self):
        return self.services.first()
