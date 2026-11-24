from django.db import models
from courses.models import Module


class Quiz(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("closed", "Closed"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="quizzes",
    )

    total_marks = models.PositiveIntegerField(default=0)
    duration_minutes = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["module", "title"],
                name="unique_quiz_per_module",
            )
        ]

    def __str__(self):
        return self.title