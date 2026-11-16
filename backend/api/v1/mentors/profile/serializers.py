from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError as DjangoValidationError

from mentors.models import MentorProfile


class MentorProfileSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MentorProfile
        fields = [
            "id",
            "user_id",
            "designation",
            "bio",
            "profile_image",
            "years_of_experience",
            "expertise",
            "linkedin_url",
            "github_url",
            "portfolio_url",
            "languages",
            "is_available",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user_id", "created_at", "updated_at"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj) -> str:
        return str(obj.id)

    @extend_schema_field(OpenApiTypes.STR)
    def get_user_id(self, obj) -> str:
        return str(obj.user.id)

    def validate_linkedin_url(self, value):
        if value and not _is_valid_url(value):
            raise serializers.ValidationError("Invalid LinkedIn URL.")
        return value

    def validate_github_url(self, value):
        if value and not _is_valid_url(value):
            raise serializers.ValidationError("Invalid GitHub URL.")
        return value

    def validate_portfolio_url(self, value):
        if value and not _is_valid_url(value):
            raise serializers.ValidationError("Invalid portfolio URL.")
        return value

    def validate_profile_image(self, value):
        if value and not _is_valid_url(value):
            raise serializers.ValidationError("Invalid image URL.")
        return value

    def validate_expertise(self, value):
        if value is None:
            return []
        if not isinstance(value, list):
            raise serializers.ValidationError("Expertise must be a list of strings.")
        if not all(isinstance(item, str) for item in value):
            raise serializers.ValidationError("Expertise items must be strings.")
        return value

    def validate_languages(self, value):
        if value is None:
            return []
        if not isinstance(value, list):
            raise serializers.ValidationError("Languages must be a list of strings.")
        if not all(isinstance(item, str) for item in value):
            raise serializers.ValidationError("Language items must be strings.")
        return value

    def validate_years_of_experience(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Years of experience cannot be negative.")
        return value


def _is_valid_url(value):
    try:
        URLValidator()(value)
        return True
    except DjangoValidationError:
        return False


class PublicMentorProfileSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = MentorProfile
        fields = [
            "id",
            "user_id",
            "name",
            "designation",
            "bio",
            "profile_image",
            "years_of_experience",
            "expertise",
            "linkedin_url",
            "github_url",
            "portfolio_url",
            "languages",
            "is_available",
            "created_at",
        ]
        read_only_fields = fields

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj) -> str:
        return str(obj.id)

    @extend_schema_field(OpenApiTypes.STR)
    def get_user_id(self, obj) -> str:
        return str(obj.user.id)

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj) -> str:
        return obj.user.get_full_name() or obj.user.username