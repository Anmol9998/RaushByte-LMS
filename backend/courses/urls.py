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
#from .test_upload import TestUploadView
urlpatterns = [
    # ==========================
    # Course APIs
    # ==========================
    #path("test-upload/", TestUploadView.as_view()),

    path("", CourseListCreateView.as_view(), name="course-list"),

    # ==========================
    # Module APIs
    # ==========================
    path(
        "modules/",
        ModuleListCreateView.as_view(),
        name="module-list",
    ),
    path(
        "modules/<str:pk>/",
        ModuleDetailView.as_view(),
        name="module-detail",
    ),

    # ==========================
    # Lesson APIs
    # ==========================
    path(
        "lessons/",
        LessonListCreateView.as_view(),
        name="lesson-list",
    ),
    path(
        "lessons/<str:pk>/",
        LessonDetailView.as_view(),
        name="lesson-detail",
    ),

    # ==========================
    # Lesson Resource APIs
    # ==========================
    path(
        "resources/",
        LessonResourceListCreateView.as_view(),
        name="resource-list",
    ),
    path(
        "resources/<str:pk>/",
        LessonResourceDetailView.as_view(),
        name="resource-detail",
    ),

    # ==========================
    # Course Detail (KEEP LAST)
    # ==========================
    path(
        "<str:pk>/",
        CourseDetailView.as_view(),
        name="course-detail",
    ),
]