from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from assignments.models import Assignment
from courses.models import Module


class AssignmentSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    module = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all()
    )

    mentor = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = [
            "id",
            "module",
            "mentor",
            "title",
            "description",
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

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj):
        return str(obj.id)

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_mentor(self, obj):
        if obj.mentor:
            return {
                "id": str(obj.mentor.id),
                "name": obj.mentor.get_full_name() or obj.mentor.username,
                "email": obj.mentor.email,
            }
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["module"] = {
            "id": str(instance.module.id),
            "title": instance.module.title,
        }

        return data