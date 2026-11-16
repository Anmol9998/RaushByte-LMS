from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from courses.models import Course
from mentors.models import MentorCourseAssignment


class MentorCourseSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    is_assigned = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "category",
            "duration",
            "level",
            "is_active",
            "is_assigned",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj) -> str:
        return str(obj.id)

    def get_is_assigned(self, obj) -> bool:
        return True


class MentorCourseAssignmentSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    mentor_id = serializers.SerializerMethodField(read_only=True)
    course_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MentorCourseAssignment
        fields = [
            "id",
            "mentor_id",
            "course_id",
            "responsibility",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "mentor_id", "course_id", "created_at", "updated_at"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj) -> str:
        return str(obj.id)

    @extend_schema_field(OpenApiTypes.STR)
    def get_mentor_id(self, obj) -> str:
        return str(obj.mentor.id)

    @extend_schema_field(OpenApiTypes.STR)
    def get_course_id(self, obj) -> str:
        return str(obj.course.id)


class AssignMentorToCourseSerializer(serializers.Serializer):
    mentor_id = serializers.CharField()
    responsibility = serializers.ChoiceField(
        choices=[
            ("instructor", "Lead Instructor"),
            ("co_instructor", "Co-Instructor"),
            ("guest", "Guest Mentor"),
        ],
        default="instructor",
    )