from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Course, Module, Lesson, LessonResource
from .serializers import (
    CourseSerializer,
    ModuleSerializer,
    LessonSerializer,
    LessonResourceSerializer,

)
from .permissions import IsAdminRole


# ==========================
# Course Views
# ==========================

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


# ==========================
# Module Views
# ==========================

class ModuleListCreateView(generics.ListCreateAPIView):
    queryset = Module.objects.all().order_by("order")
    serializer_class = ModuleSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]


class ModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]


# ==========================
# Lesson Views
# ==========================

class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all().order_by("order")
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]

class LessonResourceListCreateView(generics.ListCreateAPIView):
    queryset = LessonResource.objects.all().order_by("order")
    serializer_class = LessonResourceSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]


class LessonResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LessonResource.objects.all()
    serializer_class = LessonResourceSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]