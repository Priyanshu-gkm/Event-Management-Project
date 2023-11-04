from django.test import TestCase
from django.urls import reverse

from events_tickets.models import TicketType , EventTicketType , Event , Ticket
from events_tickets.model_factory import EventFactory, TicketTypeFactory , TicketFactory
from events_tickets.serializers import EventSerializer, TicketTypeSerializer
from events_tickets.setup_data import get_setup_data
from accounts.models import Account

from faker import Faker
import random
import factory

# Create your tests here.

fake = Faker()


class EventChecks(TestCase):
    def setUp(self):
        for k, v in get_setup_data().items():
            setattr(self, k, v)
        for i in range(3):
            TicketTypeFactory()

        tickets = [
            {
                "ticket_type": random.choice(
                    list(TicketType.objects.values_list("pk", flat=True))
                ),
                "price": fake.pyint(min_value=100, max_value=9999),
                "quantity": fake.pyint(min_value=10, max_value=100),
            }
            for _ in range(2)
        ]

        photos = [fake.url() for i in range(2)]

        self.event_data = factory.build(dict, FACTORY_CLASS=EventFactory)
        self.event_data["tickets"] = tickets
        self.event_data["photos"] = photos

        self.create_event_data = self.client.post(
            reverse("LC-event"),
            data=EventSerializer(data=self.event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        ).json()

        self.update_event_data = self.event_data
        self.update_event_data["name"] = "updated name"

    def test_CreateEvent_successful_organizer(self):
        response = self.client.post(
            reverse("LC-event"),
            data=EventSerializer(data=self.event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 201)

    def test_CreateEvent_successful_admin(self):
        response = self.client.post(
            reverse("LC-event"),
            data=EventSerializer(data=self.event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
        )
        self.assertEqual(response.status_code, 201)

    def test_CreateEvent_fail_attendee(self):
        response = self.client.post(
            reverse("LC-event"),
            data=EventSerializer(data=self.event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
        )
        self.assertEqual(response.status_code, 403)

    def test_CreateNewEvent_name_missing(self):
        del self.event_data["name"]
        response = self.client.post(
            reverse("LC-event"),
            data=EventSerializer(data=self.event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 400)

    def test_CreateNewEvent_date_missing(self):
        del self.event_data["date"]
        response = self.client.post(
            reverse("LC-event"),
            data=EventSerializer(data=self.event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 400)

    def test_CreateNewEvent_time_missing(self):
        del self.event_data["time"]
        response = self.client.post(
            reverse("LC-event"),
            data=EventSerializer(data=self.event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 400)

    def test_CreateNewEvent_location_missing(self):
        del self.event_data["location"]
        response = self.client.post(
            reverse("LC-event"),
            data=EventSerializer(data=self.event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 400)

    def test_CreateNewEvent_description_missing(self):
        del self.event_data["description"]
        response = self.client.post(
            reverse("LC-event"),
            data=EventSerializer(data=self.event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 400)

    def test_ListEvent_success_admin(self):
        response = self.client.get(
            reverse("LC-event"), HTTP_AUTHORIZATION=f"Token {self.admin_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_ListEvent_success_organizer(self):
        response = self.client.get(
            reverse("LC-event"), HTTP_AUTHORIZATION=f"Token {self.organizer_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_ListEvent_success_attendee(self):
        response = self.client.get(
            reverse("LC-event"), HTTP_AUTHORIZATION=f"Token {self.attendee_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_ListEvent_success_unauthenticated(self):
        response = self.client.get(reverse("LC-event"))
        self.assertEqual(response.status_code, 200)

    def test_RetrieveEvent_successful_organizer(self):
        response = self.client.get(
            reverse("RUD-event", args=[self.create_event_data["id"]]),
            data=EventSerializer(data=self.update_event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_RetrieveEvent_successful_admin(self):
        response = self.client.get(
            reverse("RUD-event", args=[self.create_event_data["id"]]),
            data=EventSerializer(data=self.update_event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_RetrieveEvent_fail_attendee(self):
        response = self.client.get(
            reverse("RUD-event", args=[self.create_event_data["id"]]),
            data=EventSerializer(data=self.update_event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
        )
        self.assertEqual(response.status_code, 403)

    def test_UpdateEvent_successful_organizer(self):
        response = self.client.patch(
            reverse("RUD-event", args=[self.create_event_data["id"]]),
            data=EventSerializer(data=self.update_event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_UpdateEvent_successful_admin(self):
        response = self.client.patch(
            reverse("RUD-event", args=[self.create_event_data["id"]]),
            data=EventSerializer(data=self.update_event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_UpdateEvent_fail_attendee(self):
        response = self.client.patch(
            reverse("RUD-event", args=[self.create_event_data["id"]]),
            data=EventSerializer(data=self.update_event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
        )
        self.assertEqual(response.status_code, 403)

    def test_DeleteEvent_successful_organizer(self):
        response = self.client.delete(
            reverse("RUD-event", args=[self.create_event_data["id"]]),
            data=EventSerializer(data=self.update_event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 204)

    def test_DeleteEvent_successful_admin(self):
        response = self.client.delete(
            reverse("RUD-event", args=[self.create_event_data["id"]]),
            data=EventSerializer(data=self.update_event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
        )
        self.assertEqual(response.status_code, 204)

    def test_DeleteEvent_fail_attendee(self):
        response = self.client.delete(
            reverse("RUD-event", args=[self.create_event_data["id"]]),
            data=EventSerializer(data=self.update_event_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
        )
        self.assertEqual(response.status_code, 403)


class TicketTypeLCViews(TestCase):
    def setUp(self):
        for k, v in get_setup_data().items():
            setattr(self, k, v)

    def test_CreateNewTicketType_admin_success(self):
        ticket_data = factory.build(dict, FACTORY_CLASS=TicketTypeFactory)
        response = self.client.post(
            reverse("LC-ticket-type"),
            data=TicketTypeSerializer(data=ticket_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
        )
        self.assertEqual(response.status_code, 201)

    def test_CreateNewTicketType_organizer_success(self):
        ticket_data = factory.build(dict, FACTORY_CLASS=TicketTypeFactory)
        response = self.client.post(
            reverse("LC-ticket-type"),
            data=TicketTypeSerializer(data=ticket_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 201)

    def test_CreateNewTicketType_attendee_fail(self):
        ticket_data = factory.build(dict, FACTORY_CLASS=TicketTypeFactory)
        response = self.client.post(
            reverse("LC-ticket-type"),
            data=TicketTypeSerializer(data=ticket_data).initial_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
        )
        self.assertEqual(response.status_code, 403)

    def test_ListTicketType_admin_success(self):
        response = self.client.get(
            reverse("LC-ticket-type"), HTTP_AUTHORIZATION=f"Token {self.admin_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_ListTicketType_organizer_success(self):
        response = self.client.get(
            reverse("LC-ticket-type"),
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_ListTicketType_attendee_fail(self):
        response = self.client.get(
            reverse("LC-ticket-type"), HTTP_AUTHORIZATION=f"Token {self.attendee_token}"
        )
        self.assertEqual(response.status_code, 403)


class TicketTypeRUDViews(TestCase):
    def setUp(self):
        for k, v in get_setup_data().items():
            setattr(self, k, v)

        self.ticket_type_id = []
        for i in range(3):
            TicketTypeFactory()
            self.ticket_type_id.append(TicketType.objects.latest("id").__dict__["id"])

        self.data = TicketType.objects.get(
            id=random.choice(self.ticket_type_id)
        ).__dict__
        self.data["name"] = fake.name()
        del self.data["_state"]

    def test_TicketType_Retrieve_admin_success(self):
        response = self.client.get(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_TicketType_Retrieve_organizer_fail(self):
        response = self.client.get(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 403)

    def test_TicketType_Retrieve_attendee_fail(self):
        response = self.client.get(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
        )
        self.assertEqual(response.status_code, 403)

    def test_TicketType_Update_admin_success(self):
        response = self.client.patch(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_TicketType_Update_organizer_fail(self):
        response = self.client.patch(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 403)

    def test_TicketType_Update_attendee_fail(self):
        response = self.client.patch(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
        )
        self.assertEqual(response.status_code, 403)

    def test_TicketType_Delete_admin_success(self):
        response = self.client.delete(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
        )
        self.assertEqual(response.status_code, 204)

    def test_TicketType_Delete_organizer_fail(self):
        response = self.client.delete(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 403)

    def test_TicketType_Delete_attendee_fail(self):
        response = self.client.delete(
            reverse("RUD-ticket-type", args=[random.choice(self.ticket_type_id)]),
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
        )
        self.assertEqual(response.status_code, 403)

class TicketLCViews(TestCase):
    @classmethod
    def setUpTestData(self):
        self.ticket_create_data = {"event": 34, "ticket": [{"type": 1, "quantity": 2}]}
        for k, v in get_setup_data().items():
            setattr(self, k, v)
        for i in range(3):
            TicketTypeFactory()

        for i in range(3):
            tickets = [
                {
                    "ticket_type": random.choice(
                        list(TicketType.objects.values_list("pk", flat=True))
                    ),
                    "price": fake.pyint(min_value=100, max_value=9999),
                    "quantity": fake.pyint(min_value=10, max_value=100),
                }
                for _ in range(2)
            ]

            photos = [fake.url() for i in range(2)]

            event_data = factory.build(dict, FACTORY_CLASS=EventFactory)
            event_data["tickets"] = tickets
            event_data["photos"] = photos
            self.client.post(
                reverse("LC-event"),
                data=EventSerializer(data=event_data).initial_data,
                content_type="application/json",
                HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
            ).json()

        for i in range(1, 4):
            event = list(Event.objects.all())[
                random.randint(1, Event.objects.count() - 1)
            ]
            customer = Account.objects.get(id=i)
            ticket_type = EventTicketType.objects.filter(event=event)[0].ticket_type
            TicketFactory(event=event, customer=customer, ticket_type=ticket_type)
        # print(Account.objects.all().values_list("id"))
        # print(Event.objects.all())
        # print(EventTicketType.objects.all())
        # print(Ticket.objects.all())

    def test_TicketList_admin_success(self):
        response = self.client.get(
            reverse("LC-ticket"), HTTP_AUTHORIZATION=f"Token {self.admin_token}"
        )
        self.assertEqual(1,2,msg="assert 1==2")
        self.assertTrue(Ticket.objects.count() == len(response.json()),msg="equal number of objects")
        self.assertEqual(response.status_code, 200)

    def test_TicketList_organizer_success(self):
        response = self.client.get(
            reverse("LC-ticket"), HTTP_AUTHORIZATION=f"Token {self.organizer_token}"
        )
        response_ids = set([i["event"] for i in response.json()])
        created_by_ids = set([Event.objects.get(id=i).created_by for i in response_ids])
        self.assertTrue(len(created_by_ids)==1)
        self.assertTrue(self.organizer_id in created_by_ids)
        self.assertFalse(self.admin_id in created_by_ids)
        self.assertFalse(self.attendee_id in created_by_ids) 
        self.assertEqual(response.status_code, 200)

    def test_TicketList_attendee_success(self):
        response = self.client.get(
            reverse("LC-ticket"), HTTP_AUTHORIZATION=f"Token {self.attendee_token}"
        )
        response_ids = set([i["customer"] for i in response.json()])
        self.assertTrue(len(response_ids)==1)
        self.assertTrue(self.attendee_id in response_ids)
        self.assertFalse(self.admin_id in response_ids)
        self.assertFalse(self.organizer_id in response_ids)
        self.assertEqual(response.status_code, 200)

    def test_TicketCreate_admin_success(self):
        response = self.client.post(
            reverse("LC-ticket"), HTTP_AUTHORIZATION=f"Token {self.admin_token}",data=self.ticket_create_data,content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_TicketCreate_organizer_success(self):
        response = self.client.post(
            reverse("LC-ticket"), HTTP_AUTHORIZATION=f"Token {self.organizer_token}",data=self.ticket_create_data,content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_TicketCreate_attendee_success(self):
        response = self.client.post(
            reverse("LC-ticket"), HTTP_AUTHORIZATION=f"Token {self.attendee_token}",data=self.ticket_create_data,content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_TicketCreate_attendee_fail_event_does_not_exist(self):
        response = self.client.post(
            reverse("LC-ticket"), HTTP_AUTHORIZATION=f"Token {self.attendee_token}",data=self.ticket_create_data,content_type='application/json'
        )
        self.assertIn("object does not exist",str(response.content))
        self.assertEqual(response.status_code, 400)

    def test_TicketCreate_attendee_fail_event_inactive(self):
        self.ticket_create_data['event']=1
        inst = Event.objects.get(id=1)
        inst.is_active=False
        inst.save()
        response = self.client.post(
            reverse("LC-ticket"), HTTP_AUTHORIZATION=f"Token {self.attendee_token}",data=self.ticket_create_data,content_type='application/json'
        )
        self.assertIn("inactive",str(response.json()))
        self.assertEqual(response.status_code, 400)

    def test_TicketCreate_attendee_fail_event_active_ticket_not_linked(self):
        ticket_type_list = [k[0]for k in list(EventTicketType.objects.filter(event=1).values_list('ticket_type'))]
        self.ticket_create_data['ticket'][0]['type']=random.randint(1000,9999)
        response = self.client.post(
            reverse("LC-ticket"), HTTP_AUTHORIZATION=f"Token {self.attendee_token}",data=self.ticket_create_data,content_type='application/json'
        )
        self.assertIn("ticket type not found",str(response.json()))
        self.assertEqual(response.status_code, 400)
