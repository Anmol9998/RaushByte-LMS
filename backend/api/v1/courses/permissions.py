from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        return (
            user.is_authenticated
            and (
                user.is_staff
                or user.is_superuser
                or getattr(user, "role", "") == "admin"
            )
        )