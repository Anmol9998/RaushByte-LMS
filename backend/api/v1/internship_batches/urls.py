from django.urls import path

from .views import InternshipBatchDetailView, InternshipBatchListCreateView

urlpatterns = [
    path("", InternshipBatchListCreateView.as_view(), name="internship-batch-list"),
    path("<str:pk>/", InternshipBatchDetailView.as_view(), name="internship-batch-detail"),
]