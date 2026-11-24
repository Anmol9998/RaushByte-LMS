from django.urls import path

from .views import OptionListCreateView, OptionDetailView

urlpatterns = [
    path("", OptionListCreateView.as_view(), name="option-list-create"),
    path("<str:pk>/", OptionDetailView.as_view(), name="option-detail"),
]