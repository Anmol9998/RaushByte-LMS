from django.db import models
from .lesson import Lesson


class LessonResource(models.Model):
    RESOURCE_TYPES = [
        ("video", "Video"),
        ("pdf", "PDF"),
        ("ppt", "PowerPoint"),
        ("text", "Text"),
        ("link", "External Link"),
        ("zip", "Source Code"),
    ]

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="resources"
    )

    title = models.CharField(max_length=200)

    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPES
    )

    file = models.FileField(
        upload_to="lesson_resources/",
        blank=True,
        null=True
    )

    external_link = models.URLField(
        blank=True,
        null=True
    )

    text_content = models.TextField(
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(default=1)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title