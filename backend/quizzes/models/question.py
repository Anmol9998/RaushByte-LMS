from django.db import models
from .quiz import Quiz


class Question(models.Model):
    QUESTION_TYPES = [
        ("single_choice", "Single Choice"),
        ("multiple_choice", "Multiple Choice"),
        ("true_false", "True/False"),
    ]

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
    )

    question_text = models.TextField()

    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        default="single_choice",
    )

    marks = models.PositiveIntegerField(default=1)

    order = models.PositiveIntegerField(default=1)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["quiz", "order"],
                name="unique_question_order_per_quiz",
            )
        ]

    def __str__(self):
        return f"Q{self.order} - {self.quiz.title}"