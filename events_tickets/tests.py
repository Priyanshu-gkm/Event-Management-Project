from django.test import TestCase
from django.urls import reverse

from events_tickets.models import TicketType
from events_tickets.model_factory import EventFactory, TicketTypeFactory 
from events_tickets.serializers import EventSerializer , TicketTypeSerializer
from events_tickets.setup_data import get_setup_data

from faker import Faker
import random
import factory

# Create your tests here.

fake = Faker()
class EventChecks(TestCase):
    
    def setUp(self):
        for k,v in get_setup_data().items():
            setattr(self,k,v)
        for i in range(3):
            TicketTypeFactory()
            
        tickets = [{"ticket_type" : random.choice(list(TicketType.objects.values_list('pk', flat=True))),
            "price" : fake.pyint(min_value=100,max_value=9999),
            "quantity" : fake.pyint(min_value=10,max_value=100)} for _ in range(2)]
        
        photos = [fake.url() for i in range(2)]
        
        self.event_data = factory.build(dict, FACTORY_CLASS=EventFactory)
        self.event_data['tickets'] =  tickets 
        self.event_data['photos'] = photos 
        
        self.create_event_data = self.client.post(reverse('LC-event'),data=EventSerializer(data=self.event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.organizer_token}').json()
        
        self.update_event_data = self.event_data
        self.update_event_data['name'] = "updated name"
        
        
        
        
    def test_CreateEvent_successful_organizer(self):
        response = self.client.post(reverse('LC-event'),data=EventSerializer(data=self.event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,201)
        
    def test_CreateEvent_successful_admin(self):
        
        response = self.client.post(reverse('LC-event'),data=EventSerializer(data=self.event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        self.assertEqual(response.status_code,201)
    
    def test_CreateEvent_fail_attendee(self):
       
        response = self.client.post(reverse('LC-event'),data=EventSerializer(data=self.event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.attendee_token}')
        self.assertEqual(response.status_code,403)

    def test_CreateNewEvent_name_missing(self):
        del self.event_data['name']
        response = self.client.post(reverse('LC-event'),data=EventSerializer(data=self.event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,400)


    def test_CreateNewEvent_date_missing(self):
        del self.event_data['date']
        response = self.client.post(reverse('LC-event'),data=EventSerializer(data=self.event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,400)

    def test_CreateNewEvent_time_missing(self):
        del self.event_data['time']
        response = self.client.post(reverse('LC-event'),data=EventSerializer(data=self.event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,400)

    def test_CreateNewEvent_location_missing(self):
        del self.event_data['location']
        response = self.client.post(reverse('LC-event'),data=EventSerializer(data=self.event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,400)

    def test_CreateNewEvent_description_missing(self):
        del self.event_data['description']
        response = self.client.post(reverse('LC-event'),data=EventSerializer(data=self.event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,400)
        
    def test_ListEvent_success_admin(self):
        response = self.client.get(reverse('LC-event'),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        self.assertEqual(response.status_code,200)
        
    def test_ListEvent_success_organizer(self):
        response = self.client.get(reverse('LC-event'),HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,200)
        
    def test_ListEvent_success_attendee(self):
        response = self.client.get(reverse('LC-event'),HTTP_AUTHORIZATION=f'Token {self.attendee_token}')
        self.assertEqual(response.status_code,200)
        
    def test_ListEvent_success_unauthenticated(self):
        response = self.client.get(reverse('LC-event'))
        self.assertEqual(response.status_code,200)
        
    def test_RetrieveEvent_successful_organizer(self):
        response = self.client.get(reverse('RUD-event',args=[self.create_event_data['id']]),data=EventSerializer(data=self.update_event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,200)
        
    def test_RetrieveEvent_successful_admin(self):
        response = self.client.get(reverse('RUD-event',args=[self.create_event_data['id']]),data=EventSerializer(data=self.update_event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        self.assertEqual(response.status_code,200)
    
    def test_RetrieveEvent_fail_attendee(self):
        response = self.client.get(reverse('RUD-event',args=[self.create_event_data['id']]),data=EventSerializer(data=self.update_event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.attendee_token}')
        self.assertEqual(response.status_code,403)
        
    def test_UpdateEvent_successful_organizer(self):
        response = self.client.patch(reverse('RUD-event',args=[self.create_event_data['id']]),data=EventSerializer(data=self.update_event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,200)
        
    def test_UpdateEvent_successful_admin(self):
        response = self.client.patch(reverse('RUD-event',args=[self.create_event_data['id']]),data=EventSerializer(data=self.update_event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        self.assertEqual(response.status_code,200)
    
    def test_UpdateEvent_fail_attendee(self):
        response = self.client.patch(reverse('RUD-event',args=[self.create_event_data['id']]),data=EventSerializer(data=self.update_event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.attendee_token}')
        self.assertEqual(response.status_code,403)
   
    def test_DeleteEvent_successful_organizer(self):
        response = self.client.delete(reverse('RUD-event',args=[self.create_event_data['id']]),data=EventSerializer(data=self.update_event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,204)
        
    def test_DeleteEvent_successful_admin(self):
        response = self.client.delete(reverse('RUD-event',args=[self.create_event_data['id']]),data=EventSerializer(data=self.update_event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        self.assertEqual(response.status_code,204)
    
    def test_DeleteEvent_fail_attendee(self):
        response = self.client.delete(reverse('RUD-event',args=[self.create_event_data['id']]),data=EventSerializer(data=self.update_event_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.attendee_token}')
        self.assertEqual(response.status_code,403)
        

class TicketTypeLCViews(TestCase):
    def setUp(self):
        for k,v in get_setup_data().items():
            setattr(self,k,v)
            
    def test_CreateNewTicketType_admin_success(self):
        ticket_data = factory.build(dict,FACTORY_CLASS=TicketTypeFactory)
        response = self.client.post(reverse('LC-ticket-type'),data=TicketTypeSerializer(data=ticket_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        self.assertEqual(response.status_code,201)
            
    def test_CreateNewTicketType_organizer_success(self):
        ticket_data = factory.build(dict,FACTORY_CLASS=TicketTypeFactory)
        response = self.client.post(reverse('LC-ticket-type'),data=TicketTypeSerializer(data=ticket_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,201)
            
    def test_CreateNewTicketType_attendee_fail(self):
        ticket_data = factory.build(dict,FACTORY_CLASS=TicketTypeFactory)
        response = self.client.post(reverse('LC-ticket-type'),data=TicketTypeSerializer(data=ticket_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.attendee_token}')
        self.assertEqual(response.status_code,403)
            
    def test_ListTicketType_admin_success(self):
        ticket_data = factory.build(dict,FACTORY_CLASS=TicketTypeFactory)
        response = self.client.get(reverse('LC-ticket-type'),data=TicketTypeSerializer(data=ticket_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        self.assertEqual(response.status_code,200)
            
    def test_ListTicketType_organizer_success(self):
        ticket_data = factory.build(dict,FACTORY_CLASS=TicketTypeFactory)
        response = self.client.get(reverse('LC-ticket-type'),data=TicketTypeSerializer(data=ticket_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,200)
            
    def test_ListTicketType_attendee_fail(self):
        ticket_data = factory.build(dict,FACTORY_CLASS=TicketTypeFactory)
        response = self.client.get(reverse('LC-ticket-type'),data=TicketTypeSerializer(data=ticket_data).initial_data,content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.attendee_token}')
        self.assertEqual(response.status_code,403)
        
class TicketTypeRUDViews(TestCase):
    def setUp(self):
        for k,v in get_setup_data().items():
            setattr(self,k,v)   

        self.ticket_type_id=[]
        for i in range(3):
            TicketTypeFactory()
            self.ticket_type_id.append(TicketType.objects.latest("id").__dict__['id'])
            
        self.data = TicketType.objects.get(id=random.choice(self.ticket_type_id)).__dict__
        self.data['name'] = fake.name()
        del self.data['_state']
            
        
    def test_TicketType_Retrieve_admin_success(self):
        response = self.client.get(reverse('RUD-ticket-type',args=[random.choice(self.ticket_type_id)]),HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        self.assertEqual(response.status_code,200)
        
    def test_TicketType_Retrieve_organizer_fail(self):
        response = self.client.get(reverse('RUD-ticket-type',args=[random.choice(self.ticket_type_id)]),HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,403)
        
    def test_TicketType_Retrieve_attendee_fail(self):
        response = self.client.get(reverse('RUD-ticket-type',args=[random.choice(self.ticket_type_id)]),HTTP_AUTHORIZATION=f'Token {self.attendee_token}')
        self.assertEqual(response.status_code,403)
        
    def test_TicketType_Update_admin_success(self):
        response = self.client.patch(reverse('RUD-ticket-type',args=[random.choice(self.ticket_type_id)]),data=self.data,content_type="application/json",HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        self.assertEqual(response.status_code,200)
        
    def test_TicketType_Update_organizer_fail(self):
        response = self.client.patch(reverse('RUD-ticket-type',args=[random.choice(self.ticket_type_id)]),data=self.data,content_type="application/json",HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,403)
        
    def test_TicketType_Update_attendee_fail(self):
        response = self.client.patch(reverse('RUD-ticket-type',args=[random.choice(self.ticket_type_id)]),data=self.data,content_type="application/json",HTTP_AUTHORIZATION=f'Token {self.attendee_token}')
        self.assertEqual(response.status_code,403)
        
    def test_TicketType_Delete_admin_success(self):
        response = self.client.delete(reverse('RUD-ticket-type',args=[random.choice(self.ticket_type_id)]),data=self.data,content_type="application/json",HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        self.assertEqual(response.status_code,204)
        
    def test_TicketType_Delete_organizer_fail(self):
        response = self.client.delete(reverse('RUD-ticket-type',args=[random.choice(self.ticket_type_id)]),data=self.data,content_type="application/json",HTTP_AUTHORIZATION=f'Token {self.organizer_token}')
        self.assertEqual(response.status_code,403)
        
    def test_TicketType_Delete_attendee_fail(self):
        response = self.client.delete(reverse('RUD-ticket-type',args=[random.choice(self.ticket_type_id)]),data=self.data,content_type="application/json",HTTP_AUTHORIZATION=f'Token {self.attendee_token}')
        self.assertEqual(response.status_code,403)
