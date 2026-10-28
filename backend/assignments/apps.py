from django.apps import AppConfig


class AssignmentsConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "assignments"