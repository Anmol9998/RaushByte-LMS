from django.apps import AppConfig


class MentorsConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "mentors"
    verbose_name = "Mentors"