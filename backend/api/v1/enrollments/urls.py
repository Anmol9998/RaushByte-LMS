from django.urls import path

from .views import (
    EnrollmentListCreateView,
    EnrollmentDetailView,
)

urlpatterns = [
    path(
        "",
        EnrollmentListCreateView.as_view(),
        name="enrollment-list-create",
    ),
    path(
        "<str:pk>/",
        EnrollmentDetailView.as_view(),
        name="enrollment-detail",
    ),
]