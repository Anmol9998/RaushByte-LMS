from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from courses.models import Enrollment
from users.models import CustomUser
from courses.models import Course


class EnrollmentSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    student = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role="student")
    )

    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all()
    )

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "student",
            "course",
            "status",
            "enrolled_at",
            "completed_at",
            "is_active",
        ]

        read_only_fields = [
            "id",
            "enrolled_at",
        ]

        validators = []

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj):
        return str(obj.id)

    def validate(self, attrs):
        student = attrs.get("student")
        course = attrs.get("course")

        queryset = Enrollment.objects.filter(
            student=student,
            course=course,
        )

        # Ignore current record during update
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                {
                    "enrollment": (
                        f"{student.get_full_name() or student.username} "
                        f"is already enrolled in "
                        f"{course.title}."
                    )
                }
            )

        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["student"] = {
            "id": str(instance.student.id),
            "name": instance.student.get_full_name()
            or instance.student.username,
            "email": instance.student.email,
        }

        data["course"] = {
            "id": str(instance.course.id),
            "title": instance.course.title,
        }

        return data