from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from progress.models import QuizCompletion
from enrollments.models import Enrollment
from quizzes.models import Quiz


class QuizCompletionSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    enrollment = serializers.PrimaryKeyRelatedField(
        queryset=Enrollment.objects.all()
    )

    quiz = serializers.PrimaryKeyRelatedField(
        queryset=Quiz.objects.all()
    )

    class Meta:
        model = QuizCompletion
        fields = [
            "id",
            "enrollment",
            "quiz",
            "completed_at",
            "is_active",
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

        data["enrollment"] = {
            "id": str(instance.enrollment.id),
            "student": (
                instance.enrollment.student.get_full_name()
                or instance.enrollment.student.username
            ),
            "course": instance.enrollment.course.title,
        }

        data["quiz"] = {
            "id": str(instance.quiz.id),
            "title": instance.quiz.title,
        }

        return data