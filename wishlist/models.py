from django.db import models
from events.models import Event
from Event_Management.settings import AUTH_USER_MODEL


# Create your models here.
class Wishlist(models.Model):
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
