from django.urls import re_path
from .views import MentorStudentsListView, MentorStudentDetailView

urlpatterns = [
    re_path(r"^$", MentorStudentsListView.as_view(), name="mentor-students-list"),
    re_path(
        r"^(?P<student_id>[^/.]+)/?$",
        MentorStudentDetailView.as_view(),
        name="mentor-student-detail",
    ),
]