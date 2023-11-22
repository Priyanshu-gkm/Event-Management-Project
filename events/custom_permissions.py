from rest_framework import permissions

class IsEventOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and obj.created_by.id == request.user.id
        )

