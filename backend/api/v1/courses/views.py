from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    JSONParser,
)
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

from courses.models import Course, Module, Lesson, LessonResource
from .serializers import (
    CourseSerializer,
    ModuleSerializer,
    LessonSerializer,
    LessonResourceSerializer,
)
from .permissions import IsAdminRole


class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all().order_by("-created_at")
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]


class ModuleListCreateView(generics.ListCreateAPIView):
    serializer_class = ModuleSerializer

    def get_queryset(self):
        queryset = Module.objects.all().order_by("order")

        course_id = self.request.query_params.get("course_id")
        if course_id:
            queryset = queryset.filter(course=course_id)

        return queryset

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]

    def perform_create(self, serializer):
        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, pk=course_id)
        serializer.save(course=course)


class ModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]


class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        queryset = Lesson.objects.all().order_by("order")

        module_id = self.request.query_params.get("module_id")
        if module_id:
            queryset = queryset.filter(module=module_id)
        return queryset
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]

    def perform_create(self, serializer):
        module_id = self.request.data.get("module")
        module = get_object_or_404(Module, pk=module_id)
        serializer.save(module=module)



class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]

    def perform_destroy(self, instance):
        # Store the file information before deleting the lesson
        file_name = instance.file.name if instance.file else None
        file_storage = instance.file.storage if instance.file else None

        # Delete the lesson from the database
        super().perform_destroy(instance)

        # Delete the uploaded file from Cloudflare R2
        if file_name and file_storage:
            try:
                file_storage.delete(file_name)
            except Exception:
                import logging
                logging.getLogger(__name__).exception(
                    "Failed to delete lesson file from storage: %s",
                    file_name
                )



class LessonResourceListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonResourceSerializer

    def get_queryset(self):
        queryset = LessonResource.objects.all().order_by("order")

        lesson_id = self.request.query_params.get("lesson_id")
        if lesson_id:
            queryset = queryset.filter(lesson=lesson_id)

        return queryset
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]

    def perform_create(self, serializer):
        lesson_id = self.request.data.get("lesson")
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        serializer.save(lesson=lesson)


class LessonResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LessonResource.objects.all()
    serializer_class = LessonResourceSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]
