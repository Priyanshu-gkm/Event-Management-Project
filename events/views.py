from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend

from events.models import Event
from events.serializers import EventSerializer
from events.custom_permissions import IsEventOwner
from events.custom_filters import EventFilter

from accounts.custom_permissions import IsAdminUser, IsOrganizer


class EventListCreate(ListCreateAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EventFilter
    search_fields = ["name", "location", "description", "created_by__username"]

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
    permission_classes = [IsAdminUser | IsEventOwner]
