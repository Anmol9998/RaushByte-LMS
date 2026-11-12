from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from courses.models import Course
from internship_batches.models import InternshipBatch


class InternshipBatchMentorSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    email = serializers.CharField()


class InternshipBatchCourseSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()


class InternshipBatchSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    mentor = serializers.SerializerMethodField()
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        required=False,
        allow_null=True,
    )
    course_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = InternshipBatch
        fields = [
            "id",
            "batch_name",
            "course",
            "course_info",
            "mentor",
            "start_date",
            "end_date",
            "max_students",
            "status",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "mentor", "created_at", "updated_at"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj) -> str:
        return str(obj.id)

    @extend_schema_field(InternshipBatchMentorSerializer(allow_null=True))
    def get_mentor(self, obj) -> dict[str, str] | None:
        if obj.mentor:
            return {
                "id": str(obj.mentor.id),
                "name": obj.mentor.get_full_name() or obj.mentor.username,
                "email": obj.mentor.email,
            }
        return None

    @extend_schema_field(InternshipBatchCourseSerializer(allow_null=True))
    def get_course_info(self, obj) -> dict[str, str] | None:
        if obj.course:
            return {
                "id": str(obj.course.id),
                "title": obj.course.title,
            }
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get("course") is not None:
            data["course"] = str(data["course"])
        return data