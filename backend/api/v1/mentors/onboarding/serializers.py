from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from mentors.models import MentorOnboardingApplication, MentorOnboardingDocument


class MentorOnboardingDocumentSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = MentorOnboardingDocument
        fields = [
            "id",
            "document_type",
            "file_url",
            "file_name",
            "file_size",
            "created_at",
        ]
        read_only_fields = fields

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj) -> str:
        return str(obj.id)


class MentorOnboardingApplicationSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    documents = MentorOnboardingDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = MentorOnboardingApplication
        fields = [
            "id",
            "status",
            "designation",
            "bio",
            "years_of_experience",
            "expertise",
            "linkedin_url",
            "github_url",
            "portfolio_url",
            "languages",
            "rejection_reason",
            "correction_notes",
            "reviewed_by",
            "reviewed_at",
            "approved_at",
            "documents",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "reviewed_by",
            "reviewed_at",
            "approved_at",
            "documents",
            "created_at",
            "updated_at",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj) -> str:
        return str(obj.id)

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


class OnboardingDocumentUploadSerializer(serializers.Serializer):
    document_type = serializers.ChoiceField(
        choices=[
            ("resume", "Resume/CV"),
            ("id_proof", "Government ID Proof"),
            ("certificate", "Professional Certificate"),
            ("other", "Other"),
        ]
    )
    file_url = serializers.URLField()
    file_name = serializers.CharField(required=False, allow_blank=True)
    file_size = serializers.IntegerField(required=False, allow_null=True, min_value=0)


class AdminOnboardingActionSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False, allow_blank=True)