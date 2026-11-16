from rest_framework.permissions import BasePermission


class IsMentor(BasePermission):
    """Allow access only to users with mentor role."""

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and getattr(user, "role", "") == "mentor"
        )


class IsMentorOwner(BasePermission):
    """
    Object-level permission: only the owner mentor can edit their profile.
    Expects the view's object to expose a ``user`` attribute linking to CustomUser.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not (user.is_authenticated and getattr(user, "role", "") == "mentor"):
            return False
        owner_user = getattr(obj, "user", None)
        if owner_user is None:
            return False
        return str(owner_user.id) == str(user.id)