from django.urls import re_path
from .views import MentorProfileView, PublicMentorProfileView

urlpatterns = [
    re_path(r"^$", MentorProfileView.as_view(), name="mentor-profile"),
    re_path(
        r"^(?P<mentor_id>[^/.]+)/?$",
        PublicMentorProfileView.as_view(),
        name="mentor-profile-public",
    ),
]