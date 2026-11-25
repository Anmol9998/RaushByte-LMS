from django.db import models
from .module import Module


class Lesson(models.Model):
    CONTENT_TYPE_CHOICES = [
        ("video", "Video"),
        ("pdf", "PDF"),
        ("ppt", "PPT"),
        ("text", "Text"),
        ("link", "Link")
        
    ]

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="lessons"
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPE_CHOICES
    )

    file = models.FileField(
        upload_to="lesson_files/",
        blank=True,
        null=True
    )

    external_link = models.URLField(blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        unique_together = ["module", "order"]

    def __str__(self):
        return self.title