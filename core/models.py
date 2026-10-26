from django.db import models


class Page(models.Model):
    """Простые текстовые страницы: о компании, политика конфиденциальности."""

    slug = models.SlugField("URL", unique=True)
    title = models.CharField("Заголовок", max_length=200)
    lead = models.TextField("Лид-абзац", blank=True)
    body = models.TextField("Текст (HTML)", blank=True)
    seo_title = models.CharField("SEO title", max_length=200, blank=True)
    seo_description = models.CharField("SEO description", max_length=300, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "страница"
        verbose_name_plural = "страницы"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        from django.urls import reverse

        route = {"o-kompanii": "about", "privacy": "privacy"}.get(self.slug)
        return reverse(route) if route else "/"
