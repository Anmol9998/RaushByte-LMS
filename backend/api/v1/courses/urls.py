from django.urls import re_path
from .views import CourseListCreateView, CourseDetailView

urlpatterns = [
    re_path(r"", CourseListCreateView.as_view(), name="course-list"),
    re_path(r"^detail/(?P<pk>[^/.]+)/?$", CourseDetailView.as_view(), name="course-detail"),
]