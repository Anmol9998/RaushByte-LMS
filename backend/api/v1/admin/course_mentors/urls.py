from django.urls import re_path
from .views import AdminCourseMentorListCreateView, AdminCourseMentorDetailView

urlpatterns = [
    re_path(
        r"^(?P<course_id>[^/.]+)/mentors/?$",
        AdminCourseMentorListCreateView.as_view(),
        name="admin-course-mentor-list-create",
    ),
    re_path(
        r"^(?P<course_id>[^/.]+)/mentors/(?P<mentor_id>[^/.]+)/?$",
        AdminCourseMentorDetailView.as_view(),
        name="admin-course-mentor-detail",
    ),
]