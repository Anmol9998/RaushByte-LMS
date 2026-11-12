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