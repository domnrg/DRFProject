from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Введите описание курса",
    )
    preview = models.ImageField(
        upload_to="materials/previews",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите картинку",
    )

    USERNAME_FIELD = "name"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural  = "Пользователи"