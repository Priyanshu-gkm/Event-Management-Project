import factory
from faker import Faker
from .models import Event,Photo,TicketType

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
    date = fake.date_this_year(after_today=True,before_today=False)
    time = fake.time()
    location = fake.city()
    description  = fake.text()