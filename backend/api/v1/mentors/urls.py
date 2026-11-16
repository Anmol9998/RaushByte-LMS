from django.urls import include, re_path

urlpatterns = [
    re_path(r"^profile/", include("api.v1.mentors.profile.urls")),
    re_path(r"^onboarding/", include("api.v1.mentors.onboarding.urls")),
    re_path(r"^courses/", include("api.v1.mentors.courses.urls")),
    re_path(r"^students/", include("api.v1.mentors.students.urls")),
]