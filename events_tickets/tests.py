from django.test import TestCase
from django.urls import reverse

from faker import Faker
import random
import factory

from Event_Management.events_tickets.models import (
    TicketType,
    Event,
    EventTicketType,
    Ticket,
    Wishlist,
)
from Event_Management.events_tickets.model_factory import (
    EventFactory,
    TicketTypeFactory,
    TicketFactory,
)
from Event_Management.events_tickets.serializers import (
    EventSerializer,
    TicketTypeSerializer,
)
from Event_Management.accounts.models import Account
from Event_Management.events_tickets.setup_data import get_setup_data


fake = Faker()


class EventChecks(TestCase):
    def setUp(self):
        for k, v in get_setup_data().items():
            setattr(self, k, v)
        for _ in range(3):
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
        for _ in range(3):
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
        for k, v in get_setup_data().items():
            setattr(self, k, v)
        for iter in range(3):
            TicketTypeFactory()

        for iter in range(3):
            ticks = list(TicketType.objects.values_list("pk", flat=True))
            tickets = [
                {
                    "ticket_type": ticks[_],
                    "price": fake.pyint(min_value=100, max_value=9999),
                    "quantity": fake.pyint(min_value=10, max_value=100),
                }
                for _ in range(1, 3)
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

        for iter in range(1, 4):
            event = list(Event.objects.all())[
                random.randint(1, Event.objects.count() - 1)
            ]
            customer = Account.objects.first()
            ticket_type = EventTicketType.objects.filter(event=event)[0].ticket_type
            TicketFactory(event=event, customer=customer, ticket_type=ticket_type)

        event = list(Event.objects.all())[random.randint(1, Event.objects.count() - 1)]
        ticket_type = EventTicketType.objects.filter(event=event)[0].ticket_type
        self.ticket_create_data = {
            "event": event.id,
            "tickets": [{"type": ticket_type.id, "quantity": 2}],
        }

    def test_TicketList_admin_success(self):
        response = self.client.get(
            reverse("LC-ticket"), HTTP_AUTHORIZATION=f"Token {self.admin_token}"
        )
        self.assertTrue(
            Ticket.objects.count() == len(response.json()),
            msg="equal number of objects",
        )
        self.assertEqual(response.status_code, 200)

    def test_TicketList_organizer_success(self):
        response = self.client.get(
            reverse("LC-ticket"), HTTP_AUTHORIZATION=f"Token {self.organizer_token}"
        )
        response_ids = set([i["event"] for i in response.json()])
        created_by_ids = set(
            [Event.objects.get(id=i).created_by.id for i in response_ids]
        )
        self.assertTrue(len(created_by_ids) == 1)
        self.assertTrue(self.organizer_id in created_by_ids)
        self.assertFalse(self.admin_id in created_by_ids)
        self.assertFalse(self.attendee_id in created_by_ids)
        self.assertEqual(response.status_code, 200)

    def test_TicketList_attendee_success(self):
        response = self.client.get(
            reverse("LC-ticket"), HTTP_AUTHORIZATION=f"Token {self.attendee_token}"
        )
        response_ids = set([i["customer"] for i in response.json()])
        self.assertTrue(len(response_ids) == 1)
        self.assertTrue(self.attendee_id in response_ids)
        self.assertFalse(self.admin_id in response_ids)
        self.assertFalse(self.organizer_id in response_ids)
        self.assertEqual(response.status_code, 200)

    def test_TicketCreate_admin_success(self):
        response = self.client.post(
            reverse("LC-ticket"),
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
            data=self.ticket_create_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_TicketCreate_organizer_success(self):
        response = self.client.post(
            reverse("LC-ticket"),
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
            data=self.ticket_create_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_TicketCreate_attendee_success(self):
        response = self.client.post(
            reverse("LC-ticket"),
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
            data=self.ticket_create_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_TicketCreate_attendee_fail_event_does_not_exist(self):
        ticket_data = self.ticket_create_data
        ticket_data["event"] = random.randint(4000, 5000)
        try:
            response = self.client.post(
                reverse("LC-ticket"),
                HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
                data=ticket_data,
                content_type="application/json",
            )
        except Exception as e:
            self.assertEqual("Event matching query does not exist.", str(e))

    def test_TicketCreate_attendee_fail_event_inactive(self):
        inst = Event.objects.first()
        inst.is_active = False
        inst.save()
        self.ticket_create_data["event"] = inst.id
        response = self.client.post(
            reverse("LC-ticket"),
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
            data=self.ticket_create_data,
            content_type="application/json",
        )
        self.assertIn("Invalid", str(response.json()))
        self.assertEqual(response.status_code, 400)

    def test_TicketCreate_attendee_fail_event_active_ticket_not_linked(self):
        self.ticket_create_data["tickets"][0]["type"] = random.randint(1000, 9999)
        response = self.client.post(
            reverse("LC-ticket"),
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
            data=self.ticket_create_data,
            content_type="application/json",
        )
        self.assertIn("matching query does not exist.", str(response.json()))
        self.assertEqual(response.status_code, 400)


class TicketRUDViews(TestCase):
    @classmethod
    def setUpTestData(self):
        for k, v in get_setup_data().items():
            setattr(self, k, v)
        for iter in range(3):
            TicketTypeFactory()

        for iter in range(3):
            ticks = list(TicketType.objects.values_list("pk", flat=True))
            tickets = [
                {
                    "ticket_type": ticks[_],
                    "price": fake.pyint(min_value=100, max_value=9999),
                    "quantity": fake.pyint(min_value=10, max_value=100),
                }
                for _ in range(1, 3)
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

        for iter in range(1, 4):
            event = list(Event.objects.all())[
                random.randint(1, Event.objects.count() - 1)
            ]
            customer = Account.objects.first()
            ticket_type = EventTicketType.objects.filter(event=event)[0].ticket_type
            TicketFactory(event=event, customer=customer, ticket_type=ticket_type)

        event = list(Event.objects.all())[random.randint(1, Event.objects.count() - 1)]
        ticket_type = EventTicketType.objects.filter(event=event)[0].ticket_type
        self.ticket_create_data = {
            "event": event.id,
            "tickets": [{"type": ticket_type.id, "quantity": 2}],
        }

    def setUp(self):
        tickets = list(Ticket.objects.all())
        self.ticket = random.choice(tickets)

    def test_TicketRetrieve_admin_success(self):
        response = self.client.get(
            reverse("RUD-ticket", args=[self.ticket.id]),
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_TicketRetrieve_attendee_success(self):
        event = list(Event.objects.all())[random.randint(1, Event.objects.count() - 1)]
        customer = self.attendee_user
        ticket_type = EventTicketType.objects.filter(event=event)[0].ticket_type
        ticket = TicketFactory(event=event, customer=customer, ticket_type=ticket_type)
        response = self.client.get(
            reverse("RUD-ticket", args=[ticket.id]),
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_TicketRetrieve_attendee_fail(self):
        att_user = Account.objects.create_user(
            email="attendeeTest1@gmail.com",
            username="attendeeTest1",
            password="Test@Abcd",
            fname="att3",
            lname="dee3",
            gender="Female",
            role="ATTENDEE",
        )
        attendee_data = {"username": "attendeeTest1", "password": "Test@Abcd"}
        response = self.client.post(
            path=reverse("user_login"),
            data=attendee_data,
            content_type="application/json",
        )
        attendee_token = response.json()["token"]
        response = self.client.get(
            reverse("RUD-ticket", args=[self.ticket.id]),
            HTTP_AUTHORIZATION=f"Token {attendee_token}",
        )
        self.assertEqual(response.status_code, 403)

    def test_TicketRetrieve_organizer_success(self):
        response = self.client.get(
            reverse("RUD-ticket", args=[self.ticket.id]),
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_TicketRetrieve_organizer_fail(self):
        org_user = Account.objects.create_user(
            email="orgTest2@gmail.com",
            username="orgTest2",
            password="Test@Abcd",
            fname="att3",
            lname="dee3",
            gender="Female",
            role="ORGANIZER",
        )
        org_data = {"username": "orgTest2", "password": "Test@Abcd"}
        response = self.client.post(
            path=reverse("user_login"), data=org_data, content_type="application/json"
        )
        org_token = response.json()["token"]
        response = self.client.get(
            reverse("RUD-ticket", args=[self.ticket.id]),
            HTTP_AUTHORIZATION=f"Token {org_token}",
        )
        self.assertEqual(response.status_code, 403)


class WishlistViews(TestCase):
    @classmethod
    def setUpTestData(self):
        for k, v in get_setup_data().items():
            setattr(self, k, v)
        for iter in range(3):
            TicketTypeFactory()

        for iter in range(3):
            ticks = list(TicketType.objects.values_list("pk", flat=True))
            tickets = [
                {
                    "ticket_type": ticks[_],
                    "price": fake.pyint(min_value=100, max_value=9999),
                    "quantity": fake.pyint(min_value=10, max_value=100),
                }
                for _ in range(1, 3)
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

        for id in range(1, 4):
            Wishlist.objects.create(
                created_by=Account.objects.get(id=id), event=Event.objects.get(id=id)
            )

    def test_addItem_fail_login_required(self):
        response = self.client.post(
            reverse("LC-wishlist"),
            data={"event": random.randint(1, 3)},
            content_type="applicatin/json",
        )
        self.assertEqual(response.status_code, 401)

    def test_addItem_organizer_success(self):
        response = self.client.post(
            reverse("LC-wishlist"),
            data={"event": random.randint(1, 3)},
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_addItem_attendee_success(self):
        response = self.client.post(
            reverse("LC-wishlist"),
            data={"event": random.randint(1, 3)},
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_addItem_admin_success(self):
        response = self.client.post(
            reverse("LC-wishlist"),
            data={"event": random.randint(1, 3)},
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_addItem_admin_fail_event_not_exists(self):
        response = self.client.post(
            reverse("LC-wishlist"),
            data={"event": random.randint(1000, 3000)},
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_ViewItem_admin_success(self):
        response = self.client.get(
            reverse("LC-wishlist"), HTTP_AUTHORIZATION=f"Token {self.admin_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_ViewItem_attendee_success(self):
        response = self.client.get(
            reverse("LC-wishlist"), HTTP_AUTHORIZATION=f"Token {self.attendee_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_ViewItem_organizer_success(self):
        response = self.client.get(
            reverse("LC-wishlist"), HTTP_AUTHORIZATION=f"Token {self.organizer_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_ViewItem_organizer_fail_user_admin(self):
        response = self.client.get(
            reverse("LC-wishlist"), HTTP_AUTHORIZATION=f"Token {self.organizer_token}"
        )
        resp = [event["id"] for event in response.json()]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.attendee_id in resp)
        self.assertFalse(self.admin_id in resp)

    def test_ViewItem_attendee_fail_organizer_admin(self):
        response = self.client.get(
            reverse("LC-wishlist"), HTTP_AUTHORIZATION=f"Token {self.attendee_token}"
        )
        resp = [event["id"] for event in response.json()]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.organizer_id in resp)
        self.assertFalse(self.admin_id in resp)

    def test_ViewItem_admin_fail_user_organizer(self):
        response = self.client.get(
            reverse("LC-wishlist"), HTTP_AUTHORIZATION=f"Token {self.admin_token}"
        )
        resp = [event["id"] for event in response.json()]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.attendee_id in resp)
        self.assertFalse(self.organizer_id in resp)

    def test_DeleteItem_organizer_success(self):
        response = self.client.delete(
            reverse("D-wishlist", args=[self.organizer_id]),
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 204)

    def test_DeleteItem_organizer_fail_admin(self):
        response = self.client.delete(
            reverse("D-wishlist", args=[self.admin_id]),
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_DeleteItem_organizer_fail_attendee(self):
        response = self.client.delete(
            reverse("D-wishlist", args=[self.attendee_id]),
            HTTP_AUTHORIZATION=f"Token {self.organizer_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_DeleteItem_attendee_success(self):
        response = self.client.delete(
            reverse("D-wishlist", args=[self.attendee_id]),
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 204)

    def test_DeleteItem_attendee_fail_admin(self):
        response = self.client.delete(
            reverse("D-wishlist", args=[self.admin_id]),
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_DeleteItem_attendee_fail_organizer(self):
        response = self.client.delete(
            reverse("D-wishlist", args=[self.organizer_id]),
            HTTP_AUTHORIZATION=f"Token {self.attendee_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_DeleteItem_admin_success(self):
        response = self.client.delete(
            reverse("D-wishlist", args=[self.admin_id]),
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 204)

    def test_DeleteItem_admin_fail_organizer(self):
        response = self.client.delete(
            reverse("D-wishlist", args=[self.organizer_id]),
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_DeleteItem_admin_fail_attendee(self):
        response = self.client.delete(
            reverse("D-wishlist", args=[self.attendee_id]),
            HTTP_AUTHORIZATION=f"Token {self.admin_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
