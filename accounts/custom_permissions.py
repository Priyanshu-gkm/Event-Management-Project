from rest_framework import permissions


class IsSameUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.id == view.kwargs.get("pk"))


class IsAdminUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and (request.user.role == "ADMIN" or request.user.is_superuser)
        )

class IsOrganizer(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user has a 'organizer' role
        return bool(request.user.is_authenticated and request.user.role == "ORGANIZER")