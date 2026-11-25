from decimal import Decimal, ROUND_HALF_UP

from django.db import transaction
from django.utils import timezone

from assignments.models import Assignment
from courses.models import Lesson
from progress.models import Progress
from quizzes.models import Quiz


ZERO = Decimal("0.00")
HUNDRED = Decimal("100.00")


def get_course_totals(course):
    """
    Total active learning items in a course.
    """
    total_lessons = Lesson.objects.filter(
        module__course=course,
        is_active=True,
    ).count()

    total_assignments = Assignment.objects.filter(
        module__course=course,
        is_active=True,
    ).count()

    total_quizzes = Quiz.objects.filter(
        module__course=course,
        is_active=True,
    ).count()

    return {
        "lessons": total_lessons,
        "assignments": total_assignments,
        "quizzes": total_quizzes,
        "total": total_lessons + total_assignments + total_quizzes,
    }


def get_completed_counts(progress):
    """
    Returns completed counters already stored in Progress.
    """
    return {
        "lessons": progress.completed_lessons,
        "assignments": progress.completed_assignments,
        "quizzes": progress.completed_quizzes,
        "total": (
            progress.completed_lessons
            + progress.completed_assignments
            + progress.completed_quizzes
        ),
    }


def calculate_progress_percentage(progress):
    """
    Calculate percentage from completed items vs total course items.
    """
    totals = get_course_totals(progress.enrollment.course)
    completed = get_completed_counts(progress)["total"]
    total = totals["total"]

    if total == 0:
        return ZERO

    percentage = (
        Decimal(completed) * Decimal("100") / Decimal(total)
    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return min(percentage, HUNDRED)


@transaction.atomic
def recalculate_progress(progress):
    """
    Recompute percentage and update enrollment/completion status if needed.
    """
    progress.progress_percentage = calculate_progress_percentage(progress)

    if progress.progress_percentage >= HUNDRED:
        if progress.completed_at is None:
            progress.completed_at = timezone.now()

        enrollment = progress.enrollment
        if enrollment.status != "completed":
            enrollment.status = "completed"
            if enrollment.completed_at is None:
                enrollment.completed_at = timezone.now()
            enrollment.save(update_fields=["status", "completed_at"])

    progress.save(update_fields=[
        "progress_percentage",
        "completed_at",
        "last_accessed",
    ])

    return progress


@transaction.atomic
def increment_progress(progress, field_name, amount=1):
    """
    Increment one of the counters and recalculate progress.

    field_name must be one of:
    - completed_lessons
    - completed_assignments
    - completed_quizzes
    """
    if field_name not in {
        "completed_lessons",
        "completed_assignments",
        "completed_quizzes",
    }:
        raise ValueError(f"Invalid progress field: {field_name}")

    current_value = getattr(progress, field_name, 0)
    setattr(progress, field_name, current_value + amount)
    progress.save(update_fields=[field_name])

    return recalculate_progress(progress)


def reset_progress(progress):
    """
    Optional helper if you ever need to reset progress manually.
    """
    progress.completed_lessons = 0
    progress.completed_assignments = 0
    progress.completed_quizzes = 0
    progress.progress_percentage = ZERO
    progress.completed_at = None
    progress.save(update_fields=[
        "completed_lessons",
        "completed_assignments",
        "completed_quizzes",
        "progress_percentage",
        "completed_at",
    ])
    return progress

def get_or_create_progress(enrollment):
    progress, _ = Progress.objects.get_or_create(enrollment=enrollment)
    return progress