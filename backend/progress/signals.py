from django.db.models.signals import post_save
from django.dispatch import receiver

from enrollments.models import Enrollment
from progress.models import Progress


@receiver(post_save, sender=Enrollment)
def create_progress(sender, instance, created, **kwargs):
    """
    Automatically create a Progress record
    whenever a new Enrollment is created.
    """
    if created:
        Progress.objects.create(
            enrollment=instance
        )