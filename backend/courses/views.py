from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Course
from .serializers import CourseSerializer
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