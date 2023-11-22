from django.db import models

from Event_Management.settings import AUTH_USER_MODEL


class TicketType(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    is_active = models.BooleanField(default=True, verbose_name="active")

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class Ticket(models.Model):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE)
    customer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(
        TicketType, verbose_name="ticket", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_active = models.BooleanField(default=True, verbose_name="active")
    archive = models.BooleanField(default=False, verbose_name="archive")

    def delete(self, *args, **kwargs):
        self.archive = True
        self.save()
