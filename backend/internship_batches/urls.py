from django.urls import path
from .views import InternshipBatchListCreateView, InternshipBatchDetailView

urlpatterns = [
    path("", InternshipBatchListCreateView.as_view(), name="batch-list"),
    path("<str:pk>/", InternshipBatchDetailView.as_view(), name="batch-detail"),
]