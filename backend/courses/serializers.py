from rest_framework import serializers
from .models import Course, Module, Lesson, LessonResource


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


class ModuleSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = [
            "id",
            "course",
            "title",
            "description",
            "order",
            "is_active",
        ]

    def get_id(self, obj):
        return str(obj.id)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["course"] = {
            "id": str(instance.course.id),
            "title": instance.course.title,
        }
        return data


class LessonSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            "id",
            "module",
            "title",
            "description",
            "order",
            "content_type",
            "file",
            "external_link",
            "text_content",
            "is_active",
        ]

    def get_id(self, obj):
        return str(obj.id)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["module"] = {
            "id": str(instance.module.id),
            "title": instance.module.title,
        }
        return data

class LessonResourceSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = LessonResource
        fields = [
            "id",
            "lesson",
            "title",
            "resource_type",
            "file",
            "external_link",
            "text_content",
            "order",
            "is_active",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]

    def get_id(self, obj):
        return str(obj.id)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["lesson"] = {
            "id": str(instance.lesson.id),
            "title": instance.lesson.title,
        }
        return data