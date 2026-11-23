from django.urls import path

from .views import SubmissionListCreateView, SubmissionDetailView

urlpatterns = [
    path("", SubmissionListCreateView.as_view(), name="submission-list-create"),
    path("<str:pk>/", SubmissionDetailView.as_view(), name="submission-detail"),
]