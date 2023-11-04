import factory
from faker import Faker
import random
from .models import Event, EventTicketType, Photo, Ticket, TicketType
from accounts.models import Account

fake = Faker()


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo

    image = fake.url()


class TicketTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TicketType

    name = fake.name()


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    name = fake.name()
    date = fake.date_this_year(after_today=True, before_today=False)
    time = fake.time()
    location = fake.city()
    description = fake.text()


class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    event = Event.objects.all()
    customer = Account.objects.all()
    # event = list(Event.objects.all())[random.randint(1,Event.objects.count())]
    # customer =list(Account.objects.all())[random.randint(1,Account.objects.count())]
    ticket_type = EventTicketType.objects.all()
    price = random.randint(500, 1000)
