from django.db import models
from .question import Question


class Option(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options",
    )

    option_text = models.CharField(max_length=255)

    is_correct = models.BooleanField(default=False)

    order = models.PositiveIntegerField(default=1)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["question", "order"],
                name="unique_option_order_per_question",
            )
        ]

    def __str__(self):
        return f"{self.question.question_text[:30]} - Option {self.order}"