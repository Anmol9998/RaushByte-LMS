from django.urls import path

from .views import LessonCompletionView

urlpatterns = [
    path(
        "",
        LessonCompletionView.as_view(),
        name="lesson-completion",
    ),
]