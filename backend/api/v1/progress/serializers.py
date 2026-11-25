from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from progress.models import Progress
from enrollments.models import Enrollment


class ProgressSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    enrollment = serializers.PrimaryKeyRelatedField(
        queryset=Enrollment.objects.all()
    )

    class Meta:
        model = Progress
        fields = [
            "id",
            "enrollment",
            "completed_lessons",
            "completed_assignments",
            "completed_quizzes",
            "progress_percentage",
            "last_accessed",
            "completed_at",
            "is_active",
        ]

        read_only_fields = [
            "id",
            "last_accessed",
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

        return data