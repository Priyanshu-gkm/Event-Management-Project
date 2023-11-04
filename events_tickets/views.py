from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from events_tickets.models import Event, TicketType, Ticket
from events_tickets.serializers import (
    EventSerializer,
    TicketSerializer,
    TicketTypeSerializer,
)
from events_tickets.custom_permissions import IsOrganizer, IsOwner, IsAdminUser


class TicketTypeLC(ListCreateAPIView):
    serializer_class = TicketTypeSerializer
    queryset = TicketType.objects.all()
    permission_classes = [IsAdminUser | IsOrganizer]


class TicketTypeRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = TicketTypeSerializer
    queryset = TicketType.objects.all()
    permission_classes = [IsAdminUser]


class EventListCreate(ListCreateAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            # AllowAny for GET requests
            return [AllowAny()]
        elif self.request.method == "POST":
            # only admin or an organizer can create an event
            perms = IsOrganizer | IsAdminUser
            return [perms()]
        return super().get_permissions()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        event_data = request.data
        event_data["created_by"] = request.user.id
        serializer = self.get_serializer(data=event_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventRUD(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser | IsOwner]


class TicketLC(ListCreateAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()


class TicketRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
