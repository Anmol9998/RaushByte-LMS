from django.urls import re_path
from .views import (
    MentorOnboardingApplicationView,
    MentorOnboardingStatusView,
    MentorOnboardingDocumentListCreateView,
    MentorOnboardingDocumentDeleteView,
)

urlpatterns = [
    re_path(r"^$", MentorOnboardingApplicationView.as_view(), name="mentor-onboarding-application"),
    re_path(r"^status/?$", MentorOnboardingStatusView.as_view(), name="mentor-onboarding-status"),
    re_path(r"^documents/?$", MentorOnboardingDocumentListCreateView.as_view(), name="mentor-onboarding-documents"),
    re_path(
        r"^documents/(?P<doc_id>[^/.]+)/?$",
        MentorOnboardingDocumentDeleteView.as_view(),
        name="mentor-onboarding-document-delete",
    ),
]