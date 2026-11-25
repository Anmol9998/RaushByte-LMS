from rest_framework.permissions import BasePermission


class IsAuthenticatedUser(BasePermission):
    """
    Temporary permission for development.
    Allows any authenticated user.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated