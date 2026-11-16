from rest_framework.permissions import BasePermission


class IsMentor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and getattr(user, "role", "") == "mentor"


class IsAssignedCourseMentor(BasePermission):
    """
    Object-level permission: mentor must be assigned to the course.
    Expects the course object; checks MentorCourseAssignment for (mentor=request.user, course=obj).
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not (user.is_authenticated and getattr(user, "role", "") == "mentor"):
            return False
        from mentors.models import MentorCourseAssignment

        return MentorCourseAssignment.objects.filter(
            mentor=user, course=obj, is_deleted=False, is_active=True
        ).exists()