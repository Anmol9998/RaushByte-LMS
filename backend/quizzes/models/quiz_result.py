from django.db import models

from .quiz_attempt import QuizAttempt


class QuizResult(models.Model):
    STATUS_CHOICES = [
        ("passed", "Passed"),
        ("failed", "Failed"),
    ]

    quiz_attempt = models.OneToOneField(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name="result",
    )

    total_questions = models.PositiveIntegerField(default=0)

    correct_answers = models.PositiveIntegerField(default=0)

    wrong_answers = models.PositiveIntegerField(default=0)

    total_marks = models.PositiveIntegerField(default=0)

    obtained_marks = models.PositiveIntegerField(default=0)

    percentage = models.FloatField(default=0)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="failed",
    )

    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-completed_at"]

    def __str__(self):
        return f"{self.quiz_attempt.student.username} - {self.quiz_attempt.quiz.title}"