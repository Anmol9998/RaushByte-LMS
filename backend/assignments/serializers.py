from rest_framework import serializers
from .models import Assignment
from courses.models import Module



class AssignmentSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    mentor = serializers.SerializerMethodField()

    

    module = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all(),
        required=True
    )

    module_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Assignment
        fields = [
            "id",
            "title",
            "description",
            "module",
            "module_info",
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

    


    def get_module_info(self, obj):
        if obj.module:
            return {
                "id": str(obj.module.id),
                "title": obj.module.title,
            }
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get("module") is not None:
            data["module"] = str(data["module"])
        return data