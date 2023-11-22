from rest_framework import serializers

from events.models import Photo, Event, EventTicketType
from events.custom_validators import validate_date_greater_than_today

from tickets.models import TicketType


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = "__all__"

    def to_representation(self, obj):
        ret = super(PhotoSerializer, self).to_representation(obj)
        if self.context.get("from") == "get_photos":
            ret.pop("event")
        return ret


class EventTicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTicketType
        fields = ["id", "event", "ticket_type", "price", "quantity", "is_active"]

    def to_representation(self, obj):
        ret = super(EventTicketTypeSerializer, self).to_representation(obj)
        if self.context.get("from") == "get_tickets":
            ret.pop("event")

        ret["ticket_type"] = TicketType.objects.get(id=ret["ticket_type"]).name
        return ret


class EventSerializer(serializers.ModelSerializer):
    date = serializers.DateField(validators=[validate_date_greater_than_today])
    photos = serializers.SerializerMethodField()
    tickets = serializers.SerializerMethodField()

    def get_tickets(self, obj):
        tickets = EventTicketType.objects.filter(event=obj)
        return EventTicketTypeSerializer(
            tickets, many=True, read_only=True, context={"from": "get_tickets"}
        ).data

    def get_photos(self, obj):
        photos = Photo.objects.filter(event=obj)
        obj = PhotoSerializer(
            photos, many=True, read_only=True, context={"from": "get_photos"}
        ).data
        return obj

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "date",
            "time",
            "location",
            "description",
            "photos",
            "created_by",
            "is_active",
            "tickets",
        ]

    def save_photos(self, photo_data, event_id):
        img_obj = []
        for i in photo_data:
            img_obj.append({"event": event_id, "image": i})
        serializer = PhotoSerializer(data=img_obj, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def create_event_tickets(self, tickets_data, event_id):
        for i in tickets_data:
            i["event"] = event_id
        serializer = EventTicketTypeSerializer(data=tickets_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def save(self, **kwargs):
        if self.instance:
            # If the instance exists, update the fields with the validated data
            for attr, value in self.validated_data.items():
                setattr(self.instance, attr, value)
            self.instance.save()

        else:
            request = self.context.get("request")
            photo_data = request.data["photos"]
            tickets_data = request.data["tickets"]
            event_data = request.data
            del event_data["photos"]
            del event_data["tickets"]
            instance_obj = super().save(**kwargs)
            try:
                self.save_photos(photo_data, instance_obj.id)
                self.create_event_tickets(tickets_data, instance_obj.id)

            except Exception as e:
                raise e

    def to_representation(self, obj):
        ret = super(EventSerializer, self).to_representation(obj)
        viewer_id = (
            self.context.get("request").__dict__["parser_context"]["request"].user.id
        )
        if viewer_id == obj.created_by.id:
            ret.pop("created_by")
        if ret["is_active"] == False:
            ret.pop("tickets")
        return ret
