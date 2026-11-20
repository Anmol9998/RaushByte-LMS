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



class Module(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="modules",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        unique_together = ["course", "order"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    CONTENT_TYPE_CHOICES = [
        ("video", "Video"),
        ("pdf", "PDF"),
        ("ppt", "PPT"),
        ("text", "Text"),
        ("link", "Link"),
        ("quiz", "Quiz"),
        ("assignment", "Assignment"),
    ]

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)
    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPE_CHOICES,
    )
    file = models.FileField(
        upload_to="lesson_files/",
        blank=True,
        null=True,
    )
    external_link = models.URLField(blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        unique_together = ["module", "order"]

    def __str__(self):
        return self.title


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
        related_name="resources",
    )
    title = models.CharField(max_length=200)
    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPES,
    )
    file = models.FileField(
        upload_to="lesson_resources/",
        blank=True,
        null=True,
    )
    external_link = models.URLField(blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title
