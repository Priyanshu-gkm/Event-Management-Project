from django.db import models
from Event_Management.settings import AUTH_USER_MODEL


class TicketType(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    is_active = models.BooleanField(default=True, verbose_name="active")

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class Event(models.Model):
    name = models.CharField(
        verbose_name="name", blank=False, null=False, max_length=100
    )
    date = models.DateField(verbose_name="date", blank=False, null=False)
    time = models.TimeField(verbose_name="time", blank=False, null=False)
    location = models.CharField(
        verbose_name="location", blank=False, null=False, max_length=255
    )
    description = models.TextField(verbose_name="description")
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    # tickets =  serializers.SerialzerMethodField
    # images = multiple images saving thing
    is_active = models.BooleanField(default=True, verbose_name="active")

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class EventTicketType(models.Model):
    event = models.ForeignKey(Event, verbose_name="event", on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(
        TicketType, verbose_name="ticket", on_delete=models.CASCADE
    )
    price = models.DecimalField(verbose_name="price", max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True, verbose_name="active")

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class Photo(models.Model):
    event = models.ForeignKey(Event, related_name="event_img", on_delete=models.CASCADE)
    image = models.URLField("url", null=False)


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    customer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(
        TicketType, verbose_name="ticket", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_active = models.BooleanField(default=True, verbose_name="active")
    archive = models.BooleanField(default=False, verbose_name="archive")

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class Wishlist(models.Model):
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
