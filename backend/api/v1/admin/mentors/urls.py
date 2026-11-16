from django.urls import re_path
from .views import (
    AdminMentorApplicationListView,
    AdminMentorApplicationDetailView,
    AdminMentorApplicationActionView,
    AdminMentorSuspendView,
    AdminMentorReactivateView,
)

urlpatterns = [
    re_path(r"^applications/?$", AdminMentorApplicationListView.as_view(), name="admin-mentor-application-list"),
    re_path(
        r"^applications/(?P<application_id>[^/.]+)/?$",
        AdminMentorApplicationDetailView.as_view(),
        name="admin-mentor-application-detail",
    ),
    re_path(
        r"^applications/(?P<application_id>[^/.]+)/(?P<action>approve|reject|request_correction)/?$",
        AdminMentorApplicationActionView.as_view(),
        name="admin-mentor-application-action",
    ),
    re_path(
        r"^mentors/(?P<mentor_id>[^/.]+)/suspend/?$",
        AdminMentorSuspendView.as_view(),
        name="admin-mentor-suspend",
    ),
    re_path(
        r"^mentors/(?P<mentor_id>[^/.]+)/reactivate/?$",
        AdminMentorReactivateView.as_view(),
        name="admin-mentor-reactivate",
    ),
]