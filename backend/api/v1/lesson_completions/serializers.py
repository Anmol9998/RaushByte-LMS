from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from progress.models import LessonCompletion
from enrollments.models import Enrollment
from courses.models import Lesson


class LessonCompletionSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    enrollment = serializers.PrimaryKeyRelatedField(
        queryset=Enrollment.objects.all()
    )

    lesson = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all()
    )

    class Meta:
        model = LessonCompletion
        fields = [
            "id",
            "enrollment",
            "lesson",
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

        data["lesson"] = {
            "id": str(instance.lesson.id),
            "title": instance.lesson.title,
            "module": instance.lesson.module.title,
        }

        return data