from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from courses.models import Course


class CourseMentorSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    email = serializers.CharField()


class CourseSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    mentor = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "category",
            "duration",
            "level",
            "mentor",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "mentor",
            "created_at",
            "updated_at",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj) -> str:
        return str(obj.id)

    @extend_schema_field(CourseMentorSerializer(allow_null=True))
    def get_mentor(self, obj) -> dict[str, str] | None:
        if obj.mentor:
            return {
                "id": str(obj.mentor.id),
                "name": obj.mentor.get_full_name() or obj.mentor.username,
                "email": obj.mentor.email,
            }
        return None