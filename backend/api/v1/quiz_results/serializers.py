from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from quizzes.models import QuizResult, QuizAttempt


class QuizResultSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    quiz_attempt = serializers.PrimaryKeyRelatedField(
        queryset=QuizAttempt.objects.all()
    )

    class Meta:
        model = QuizResult
        fields = [
            "id",
            "quiz_attempt",
            "total_questions",
            "correct_answers",
            "wrong_answers",
            "total_marks",
            "obtained_marks",
            "percentage",
            "status",
            "completed_at",
        ]

        read_only_fields = [
            "id",
            "completed_at",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj):
        return str(obj.id)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["quiz_attempt"] = {
            "id": str(instance.quiz_attempt.id),
            "student": instance.quiz_attempt.student.get_full_name()
            or instance.quiz_attempt.student.username,
            "quiz": instance.quiz_attempt.quiz.title,
        }

        return data