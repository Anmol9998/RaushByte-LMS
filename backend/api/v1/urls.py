from django.urls import include, path, re_path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    re_path(r'auth/', include('api.v1.auth.urls')),
    re_path(r'admin/', include('api.v1.admin.urls')),
    re_path(r'students/', include('api.v1.students.urls')),
    re_path(r'mentors/', include('api.v1.mentors.urls')),
    re_path(r"courses/", include("api.v1.courses.urls")),
    re_path(r"internship-batches/", include("api.v1.internship_batches.urls")),
    re_path(r"assignments/", include("api.v1.assignments.urls")),
    re_path(r"submissions/", include("api.v1.submissions.urls")),
    re_path(r"quizzes/", include("api.v1.quizzes.urls")),
    re_path(r"questions/", include("api.v1.questions.urls")),
    re_path(r"options/", include("api.v1.options.urls")),
    re_path(r"quiz-attempts/", include("api.v1.quiz_attempts.urls")),
    re_path(r"student-answers/", include("api.v1.student_answers.urls")),
    re_path(r"quiz-results/", include("api.v1.quiz_results.urls")),
    re_path(r"enrollments/", include("api.v1.enrollments.urls")),
    re_path(r"progress/", include("api.v1.progress.urls")),
    re_path(r"lesson-completions/", include("api.v1.lesson_completions.urls")),
    re_path(r"assignment-completions/", include("api.v1.assignment_completions.urls")),
    re_path(r"quiz-completions/", include("api.v1.quiz_completions.urls"),
),
    
    # OpenAPI Schema
    re_path(
        r"^schema/?$",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    # Swagger UI
    re_path(
        r"^docs/?$",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui",
    ),

    # ReDoc
    re_path(
        r"^redoc/?$",
        SpectacularRedocView.as_view(
            url_name="schema"
        ),
        name="redoc",
    ),
]