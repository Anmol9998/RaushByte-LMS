from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from progress.models import AssignmentCompletion
from enrollments.models import Enrollment
from assignments.models import Assignment


class AssignmentCompletionSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    enrollment = serializers.PrimaryKeyRelatedField(
        queryset=Enrollment.objects.all()
    )

    assignment = serializers.PrimaryKeyRelatedField(
        queryset=Assignment.objects.all()
    )

    class Meta:
        model = AssignmentCompletion
        fields = [
            "id",
            "enrollment",
            "assignment",
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

        data["assignment"] = {
            "id": str(instance.assignment.id),
            "title": instance.assignment.title,
        }

        return data