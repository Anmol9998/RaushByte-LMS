
from rest_framework import serializers
from enrollments.models import Enrollment
from courses.models import Course


class EnrollmentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    student = serializers.CharField(
        source="student_id",
        read_only=True,
    )

    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        pk_field=serializers.CharField(),
    )

    course_title = serializers.CharField(
        source="course.title",
        read_only=True,
    )

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "student",
            "course",
            "course_title",
            "enrolled_at",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "student",
            "enrolled_at",
            "is_active",
        ]
