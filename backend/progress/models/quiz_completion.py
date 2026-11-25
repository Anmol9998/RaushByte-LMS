from django.db import models

from enrollments.models import Enrollment
from quizzes.models import Quiz


class QuizCompletion(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="quiz_completions",
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="completions",
    )

    completed_at = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        unique_together = (
            "enrollment",
            "quiz",
        )
        ordering = ["-completed_at"]

    def __str__(self):
        return f"{self.enrollment} - {self.quiz}"