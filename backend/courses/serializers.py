from rest_framework import serializers
from .models import Course


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