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
