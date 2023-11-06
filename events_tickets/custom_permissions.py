from rest_framework import permissions


class IsOrganizer(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user has a 'organizer' role
        return bool(request.user.is_authenticated and request.user.role == "ORGANIZER")


class IsEventOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and obj.created_by.id == request.user.id
        )


class IsAdminUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and (request.user.role == "ADMIN" or request.user.is_superuser)
        )
