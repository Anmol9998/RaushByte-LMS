from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from quizzes.models import Quiz
from courses.models import Module


class QuizSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    module = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all()
    )

    class Meta:
        model = Quiz
        fields = [
            "id",
            "module",
            "title",
            "description",
            "total_marks",
            "duration_minutes",
            "status",
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

        data["module"] = {
            "id": str(instance.module.id),
            "title": instance.module.title,
        }

        return data