from django.db import models

from .quiz_attempt import QuizAttempt
from .question import Question
from .option import Option


class StudentAnswer(models.Model):
    quiz_attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="student_answers",
    )

    selected_option = models.ForeignKey(
        Option,
        on_delete=models.CASCADE,
        related_name="selected_by_students",
    )

    is_correct = models.BooleanField(default=False)

    marks_obtained = models.PositiveIntegerField(default=0)

    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["answered_at"]
        unique_together = ("quiz_attempt", "question")

    def __str__(self):
        return f"{self.quiz_attempt.id} - {self.question.question_text}"