from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from quizzes.models import Option, Question


class OptionSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all()
    )

    class Meta:
        model = Option
        fields = [
            "id",
            "question",
            "option_text",
            "is_correct",
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

        data["question"] = {
            "id": str(instance.question.id),
            "question_text": instance.question.question_text,
        }

        return data