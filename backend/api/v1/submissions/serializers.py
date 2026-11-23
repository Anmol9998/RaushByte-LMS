from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from submissions.models import Submission
from assignments.models import Assignment


class SubmissionSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    assignment = serializers.PrimaryKeyRelatedField(
        queryset=Assignment.objects.all()
    )

    student = serializers.SerializerMethodField()
    reviewed_by = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = [
            "id",
            "assignment",
            "student",
            "text_answer",
            "file",
            "status",
            "submitted_at",
            "marks_obtained",
            "feedback",
            "is_graded",
            "reviewed_by",
            "reviewed_at",
            "is_active",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "student",
            "submitted_at",
            "reviewed_by",
            "reviewed_at",
            "updated_at",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj):
        return str(obj.id)

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_student(self, obj):
        if obj.student:
            return {
                "id": str(obj.student.id),
                "name": obj.student.get_full_name() or obj.student.username,
                "email": obj.student.email,
            }
        return None

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_reviewed_by(self, obj):
        if obj.reviewed_by:
            return {
                "id": str(obj.reviewed_by.id),
                "name": obj.reviewed_by.get_full_name() or obj.reviewed_by.username,
                "email": obj.reviewed_by.email,
            }
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["assignment"] = {
            "id": str(instance.assignment.id),
            "title": instance.assignment.title,
        }

        return data