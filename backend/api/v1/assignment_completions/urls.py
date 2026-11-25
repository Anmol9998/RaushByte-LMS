from django.urls import path

from .views import AssignmentCompletionView

urlpatterns = [
    path(
        "",
        AssignmentCompletionView.as_view(),
        name="assignment-completion",
    ),
]