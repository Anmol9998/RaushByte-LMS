from rest_framework import serializers
from courses.models import Course
from .models import Assignment


class AssignmentSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    mentor = serializers.SerializerMethodField()

    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        required=False,
        allow_null=True
    )

    course_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Assignment
        fields = [
            "id",
            "title",
            "description",
            "course",
            "course_info",
            "mentor",
            "due_date",
            "total_marks",
            "status",
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

    def get_id(self, obj):
        return str(obj.id)

    def get_mentor(self, obj):
        if obj.mentor:
            return {
                "id": str(obj.mentor.id),
                "name": obj.mentor.get_full_name() or obj.mentor.username,
                "email": obj.mentor.email,
            }
        return None

    def get_course_info(self, obj):
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