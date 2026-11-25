from django.db import models

from enrollments.models import Enrollment


class Progress(models.Model):
    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="progress",
    )

    completed_lessons = models.PositiveIntegerField(default=0)

    completed_assignments = models.PositiveIntegerField(default=0)

    completed_quizzes = models.PositiveIntegerField(default=0)

    progress_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    last_accessed = models.DateTimeField(auto_now=True)

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-last_accessed"]

    def __str__(self):
        return (
            f"{self.enrollment.student.get_full_name() or self.enrollment.student.username}"
            f" - {self.enrollment.course.title}"
        )