import factory
from faker import Faker
import random
from tickets.models import Ticket, TicketType
from accounts.models import Account

fake = Faker()


class TicketTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TicketType

    name = fake.name()


class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    event = fake.name()
    customer = random.choice(Account.objects.all())
    ticket_type = fake.name()
    price = random.randint(500, 1000)
