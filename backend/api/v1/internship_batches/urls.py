from django.urls import path, re_path

from .views import InternshipBatchDetailView, InternshipBatchListCreateView

urlpatterns = [
    re_path(r"^/?$", InternshipBatchListCreateView.as_view(), name="internship-batch-list"),
    re_path(r"^detail/(?P<pk>[^/.]+)/?$", InternshipBatchDetailView.as_view(), name="internship-batch-detail"),
]