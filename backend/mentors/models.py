from django.db import models
from django.conf import settings
from django.utils import timezone
from courses.models import Course

User = settings.AUTH_USER_MODEL


class SoftDeleteManager(models.Manager):
    """Manager that excludes soft-deleted records by default."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class TimeStampedSoftDeleteModel(models.Model):
    """Abstract base with soft-delete and timestamps for mentor domain models."""

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at", "updated_at"])

    def delete(self, *args, **kwargs):
        # Soft delete instead of hard delete to preserve audit history.
        self.soft_delete()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at", "updated_at"])

class MentorOnboardingApplication(TimeStampedSoftDeleteModel):
    """Mentor onboarding/verification application (Phase 1: Mentor onboarding)."""

    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("SUBMITTED", "Submitted"),
        ("UNDER_REVIEW", "Under Review"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("NEEDS_CORRECTION", "Needs Correction"),
        ("SUSPENDED", "Suspended"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="mentor_applications",
        limit_choices_to={"role": "mentor"},
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")
    designation = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    expertise = models.JSONField(default=list)
    linkedin_url = models.URLField(max_length=500, blank=True)
    github_url = models.URLField(max_length=500, blank=True)
    portfolio_url = models.URLField(max_length=500, blank=True)
    languages = models.JSONField(default=list)
    rejection_reason = models.TextField(blank=True)
    correction_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_mentor_applications",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "mentor_onboarding_applications"
        ordering = ["-created_at"]
        verbose_name = "Mentor Onboarding Application"
        verbose_name_plural = "Mentor Onboarding Applications"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.status}"


class MentorOnboardingDocument(TimeStampedSoftDeleteModel):
    """Verification document uploaded during mentor onboarding."""

    DOCUMENT_TYPE_CHOICES = [
        ("resume", "Resume/CV"),
        ("id_proof", "Government ID Proof"),
        ("certificate", "Professional Certificate"),
        ("other", "Other"),
    ]

    application = models.ForeignKey(
        MentorOnboardingApplication,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE_CHOICES)
    file_url = models.URLField(max_length=500)
    file_name = models.CharField(max_length=255, blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = "mentor_onboarding_documents"
        ordering = ["-created_at"]
        verbose_name = "Mentor Onboarding Document"
        verbose_name_plural = "Mentor Onboarding Documents"

    def __str__(self):
        return f"{self.document_type} - {self.application.user.get_full_name() or self.application.user.username}"


class MentorCourseAssignment(TimeStampedSoftDeleteModel):
    """Admin-assigned mentor-course relationship. A mentor only manages assigned courses."""

    RESPONSIBILITY_CHOICES = [
        ("instructor", "Lead Instructor"),
        ("co_instructor", "Co-Instructor"),
        ("guest", "Guest Mentor"),
    ]

    mentor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="course_assignments",
        limit_choices_to={"role": "mentor"},
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="mentor_assignments",
    )
    responsibility = models.CharField(
        max_length=20, choices=RESPONSIBILITY_CHOICES, default="instructor"
    )
    is_active = models.BooleanField(default=True)
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="course_assignments_created",
    )

    class Meta:
        db_table = "mentor_course_assignments"
        unique_together = [("mentor", "course")]
        ordering = ["-created_at"]
        verbose_name = "Mentor Course Assignment"
        verbose_name_plural = "Mentor Course Assignments"

    def __str__(self):
        return f"{self.mentor.get_full_name() or self.mentor.username} -> {self.course.title}"


class MentorProfile(TimeStampedSoftDeleteModel):
    """Professional profile of a mentor (Phase 1: Mentor profile management)."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="mentor_profile",
        limit_choices_to={"role": "mentor"},
    )
    designation = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.URLField(max_length=500, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    expertise = models.JSONField(default=list)
    linkedin_url = models.URLField(max_length=500, blank=True)
    github_url = models.URLField(max_length=500, blank=True)
    portfolio_url = models.URLField(max_length=500, blank=True)
    languages = models.JSONField(default=list)
    is_available = models.BooleanField(default=False)

    class Meta:
        db_table = "mentor_profiles"
        verbose_name = "Mentor Profile"
        verbose_name_plural = "Mentor Profiles"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.designation or 'Mentor'}"
