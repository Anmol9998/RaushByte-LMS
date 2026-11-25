from django.db import models

from enrollments.models import Enrollment
from assignments.models import Assignment


class AssignmentCompletion(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="assignment_completions",
    )

    assignment = models.ForeignKey(
        Assignment,
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
            "assignment",
        )
        ordering = ["-completed_at"]

    def __str__(self):
        return (
            f"{self.enrollment} - {self.assignment}"
        )