from rest_framework.permissions import BasePermission


class IsMentor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and getattr(user, "role", "") == "mentor"


class IsStudentOfAssignedCourse(BasePermission):
    """
    Object-level permission: the student must be enrolled in a course assigned to the mentor.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not (user.is_authenticated and getattr(user, "role", "") == "mentor"):
            return False
        from mentors.models import MentorCourseAssignment

        assigned_course_ids = MentorCourseAssignment.objects.filter(
            mentor=user, is_deleted=False, is_active=True
        ).values_list("course_id", flat=True)
        return obj.enrollments.filter(
            course_id__in=assigned_course_ids, is_deleted=False, is_active=True
        ).exists()