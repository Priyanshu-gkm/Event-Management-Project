from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from tickets.models import Ticket, TicketType
from events.models import Event
from tickets.serializers import (
    TicketSerializer,
    TicketTypeSerializer,
    TicketDataSerializer,
)
from accounts.custom_permissions import (
    IsOrganizer,
    IsAdminUser,
)
from tickets.custom_permissions import IsTicketEventOwner, IsTicketOwner


class TicketTypeLC(ListCreateAPIView):
    serializer_class = TicketTypeSerializer
    queryset = TicketType.objects.all()
    permission_classes = [IsAdminUser | IsOrganizer]


class TicketTypeRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = TicketTypeSerializer
    queryset = TicketType.objects.all()
    permission_classes = [IsAdminUser]


class TicketLC(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TicketSerializer
        else:
            return TicketDataSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            if self.request.user.role == "ADMIN":
                return Ticket.objects.all()
            elif self.request.user.role == "ORGANIZER":
                organizer_id = self.request.user.id
                events = list(
                    Event.objects.filter(created_by=organizer_id).values_list(
                        "id", flat=True
                    )
                )
                return Ticket.objects.filter(event__in=events)
            elif self.request.user.role == "ATTENDEE":
                return Ticket.objects.filter(customer=self.request.user.id)

    def post(self, request, *args, **kwargs):
        ticket_data = request.data
        ticket_data["customer"] = request.user.id
        serializer = self.get_serializer(data=ticket_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TicketCheckIn(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOrganizer]
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def patch(self, request, *args, **kwargs):
        organizer_id = request.user.id
        events = list(
            Event.objects.filter(created_by=organizer_id).values_list("id", flat=True)
        )
        instance_id = kwargs["pk"]
        if instance_id in list(
            Ticket.objects.filter(event__in=events).values_list("id", flat=True)
        ):
            ticket_inst = Ticket.objects.get(id=instance_id)
            ticket_inst.is_active = False
            ticket_inst.save()
            return Response(
                TicketSerializer(ticket_inst).data, status=status.HTTP_200_OK
            )
        else:
            raise ValidationError(
                "you are not authorized to perform this operation on this ticket!"
            )


class TicketRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == "GET":
            perms = IsAdminUser | IsTicketOwner | IsTicketEventOwner
            return [perms()]
        return super().get_permissions()
