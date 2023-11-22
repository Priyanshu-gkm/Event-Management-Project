from rest_framework import permissions
from events.models import Event


class IsTicketOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and (obj.customer.id == request.user.id)
        )


class IsTicketEventOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        event_id = obj.event.id
        event_obj = Event.objects.get(id=event_id)
        return bool(
            request.user.is_authenticated
            and (event_obj.created_by.id == request.user.id)
        )
