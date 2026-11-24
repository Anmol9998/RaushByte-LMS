
from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from courses.models import Course, Module, Lesson, LessonResource


class CourseMentorSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    email = serializers.CharField()


class CourseSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    mentor = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id", "title", "description", "category", "duration",
            "level", "mentor", "is_active", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "mentor", "created_at", "updated_at",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj):
        return str(obj.id)

    @extend_schema_field(CourseMentorSerializer(allow_null=True))
    def get_mentor(self, obj):
        if obj.mentor:
            return {
                "id": str(obj.mentor.id),
                "name": obj.mentor.get_full_name() or obj.mentor.username,
                "email": obj.mentor.email,
            }
        return None


class ModuleSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all()
    )

    class Meta:
        model = Module
        fields = [
            "id", "course", "title", "description", "order", "is_active",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj):
        return str(obj.id)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["course"] = {
            "id": str(instance.course.id),
            "title": instance.course.title,
        }
        return data



import os

class LessonSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    module = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all()
    )
    file_name = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            "id", "module", "title", "description", "order",
            "content_type", "file", "file_name", "file_size",
            "external_link", "text_content", "is_active",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj):
        return str(obj.id)

    @extend_schema_field(OpenApiTypes.STR)
    def get_file_name(self, obj):
        if obj.file:
            return os.path.basename(obj.file.name)
        return None

    @extend_schema_field(OpenApiTypes.INT)
    def get_file_size(self, obj):
        if obj.file:
            try:
                return obj.file.size
            except (OSError, ValueError):
                return None
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["module"] = {
            "id": str(instance.module.id),
            "title": instance.module.title,
        }
        return data



class LessonResourceSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    lesson = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all()
    )

    class Meta:
        model = LessonResource
        fields = [
            "id", "lesson", "title", "resource_type", "file",
            "external_link", "text_content", "order",
            "is_active", "created_at",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj):
        return str(obj.id)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["lesson"] = {
            "id": str(instance.lesson.id),
            "title": instance.lesson.title,
        }
        return data
