from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from quizzes.models import Question, Quiz


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    quiz = serializers.PrimaryKeyRelatedField(
        queryset=Quiz.objects.all()
    )

    class Meta:
        model = Question
        fields = [
            "id",
            "quiz",
            "question_text",
            "question_type",
            "marks",
            "order",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj):
        return str(obj.id)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["quiz"] = {
            "id": str(instance.quiz.id),
            "title": instance.quiz.title,
        }

        return data