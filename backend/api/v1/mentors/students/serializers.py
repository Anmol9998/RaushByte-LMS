from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from django.contrib.auth import get_user_model

User = get_user_model()


class MentorStudentSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "is_active",
            "date_joined",
        ]
        read_only_fields = fields

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj) -> str:
        return str(obj.id)