from django.urls import path

from .views import QuestionListCreateView, QuestionDetailView

urlpatterns = [
    path("", QuestionListCreateView.as_view(), name="question-list-create"),
    path("<str:pk>/", QuestionDetailView.as_view(), name="question-detail"),
]