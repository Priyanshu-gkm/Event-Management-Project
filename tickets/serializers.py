from rest_framework import serializers

from events.models import EventTicketType, Event
from tickets.models import Ticket, TicketType


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

    def save(self, **kwargs):
        if self.instance:
            for attr, value in self.validated_data.items():
                setattr(self.instance, attr, value)
            self.instance.save()
        else:
            request_data = self.validated_data
            try:
                event_inst = EventTicketType.objects.get(
                    event=request_data["event"], ticket_type=request_data["ticket_type"]
                )
                quantity = event_inst.quantity
                event_inst.quantity = quantity - 1
                event_inst.save()
                super().save(**kwargs)
            except Exception as e:
                raise e


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ["id", "name", "is_active"]


class TicketDataSerializer(serializers.Serializer):
    event = serializers.IntegerField()
    tickets = serializers.ListField()

    def validate_event(self, attrs):
        request_data = self.context.get("request").data
        event_id = request_data.get("event")
        try:
            event_inst = Event.objects.get(id=event_id)
        except Event.DoesNotExist as e:
            raise serializers.ValidationError(e)
        if event_inst.is_active == False:
            raise serializers.ValidationError("Invalid Event", code=400)
        return super().validate(attrs)

    def validate_tickets(self, attrs):
        request_data = self.context.get("request").data
        event_id = request_data.get("event")

        allowed_tickets = list(
            EventTicketType.objects.filter(event=event_id).values(
                "ticket_type", "quantity"
            )
        )
        if len(allowed_tickets) < 1:
            raise serializers.ValidationError(
                "No Ticket Available for this event", code=400
            )
        requested_tickets = request_data.get("tickets")
        for ticket in requested_tickets:
            try:
                obj = EventTicketType.objects.get(
                    event=event_id, ticket_type=ticket["type"]
                )
            except EventTicketType.DoesNotExist as e:
                raise serializers.ValidationError(e)

            if ticket["quantity"] <= obj.quantity:
                pass
            else:
                raise serializers.ValidationError(
                    detail="{} ticket type {} tickets are not available for event {}".format(
                        ticket["quantity"], ticket["type"], event_id
                    ),
                    code=400,
                )
        return super().validate(attrs)

    def save(self, **kwargs):
        request_data = self.context.get("request").data
        customer_id = request_data.get("customer")
        event_id = request_data.get("event")
        requested_tickets = request_data.get("tickets")
        for ticket in requested_tickets:
            obj = EventTicketType.objects.get(
                event=event_id, ticket_type=ticket["type"]
            )
            for i in range(ticket["quantity"]):
                serializer = TicketSerializer(
                    data={
                        "event": event_id,
                        "ticket_type": ticket["type"],
                        "customer": customer_id,
                        "price": obj.price,
                    }
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
        return serializer.data
