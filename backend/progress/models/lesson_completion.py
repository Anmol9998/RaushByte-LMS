from django.db import models

from courses.models import Lesson
from enrollments.models import Enrollment


class LessonCompletion(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="lesson_completions",
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="lesson_completions",
    )

    completed_at = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["-completed_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["enrollment", "lesson"],
                name="unique_lesson_completion",
            )
        ]

    def __str__(self):
        return (
            f"{self.enrollment.student.get_full_name() or self.enrollment.student.username}"
            f" - {self.lesson.title}"
        )