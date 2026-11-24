from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from quizzes.models import QuizAttempt, Quiz
from users.models import CustomUser


class QuizAttemptSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    student = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all()
    )

    quiz = serializers.PrimaryKeyRelatedField(
        queryset=Quiz.objects.all()
    )

    class Meta:
        model = QuizAttempt
        fields = [
            "id",
            "student",
            "quiz",
            "status",
            "started_at",
            "submitted_at",
            "score",
        ]

        read_only_fields = [
            "id",
            "started_at",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj):
        return str(obj.id)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["student"] = {
            "id": str(instance.student.id),
            "name": instance.student.get_full_name()
            or instance.student.username,
        }

        data["quiz"] = {
            "id": str(instance.quiz.id),
            "title": instance.quiz.title,
        }

        return data