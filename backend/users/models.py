from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("mentor", "Mentor"),
        ("admin", "Admin"),
    ]

    email = models.EmailField(unique=True)


    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="student",
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.username