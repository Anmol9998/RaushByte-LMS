
from django.urls import path

from .views import (
    CourseListCreateView,
    CourseDetailView,
    ModuleListCreateView,
    ModuleDetailView,
    LessonListCreateView,
    LessonDetailView,
    LessonResourceListCreateView,
    LessonResourceDetailView,
)

urlpatterns = [
    # Courses
    path("", CourseListCreateView.as_view(), name="course-list"),
    path("detail/<str:pk>/", CourseDetailView.as_view(), name="course-detail"),

    # Modules
    path("modules/", ModuleListCreateView.as_view(), name="module-list"),
    path("modules/<str:pk>/", ModuleDetailView.as_view(), name="module-detail"),

    # Lessons
    path("lessons/", LessonListCreateView.as_view(), name="lesson-list"),
    path("lessons/<str:pk>/", LessonDetailView.as_view(), name="lesson-detail"),

    # Lesson Resources
    path("resources/", LessonResourceListCreateView.as_view(), name="resource-list"),
    path("resources/<str:pk>/", LessonResourceDetailView.as_view(), name="resource-detail"),
]
