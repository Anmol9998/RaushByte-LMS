from django.urls import path

from .views import (
    StudentAnswerListCreateView,
    StudentAnswerDetailView,
)

urlpatterns = [
    path(
        "",
        StudentAnswerListCreateView.as_view(),
        name="student-answer-list-create",
    ),
    path(
        "<str:pk>/",
        StudentAnswerDetailView.as_view(),
        name="student-answer-detail",
    ),
]