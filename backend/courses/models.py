from django.db import models
from django.conf import settings


class Course(models.Model):
    LEVEL_CHOICES = [
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    category = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default="Beginner",
    )

    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title