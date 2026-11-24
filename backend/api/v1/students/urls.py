
from django.urls import path
from .views import EnrollmentListCreateView

urlpatterns = [
    path(
        "enrollments/",
        EnrollmentListCreateView.as_view(),
        name="student-enrollments",
    ),
]
