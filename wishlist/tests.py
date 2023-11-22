from django.test import TestCase
from django.urls import reverse

from faker import Faker
import random

from accounts.models import Account
from events.setup_data import get_setup_data
from events.models import Event
from events.model_factory import EventFactory
from wishlist.models import Wishlist


fake = Faker()


# Create your tests here.
class WishlistViews(TestCase):
    @classmethod
    def setUpTestData(self):
        for k, v in get_setup_data().items():
            setattr(self, k, v)
        for id in range(1, 4):
            Wishlist.objects.create(
                created_by=Account.objects.get(id=id), event=EventFactory(created_by=Account.objects.get(id=id))
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
        resp = [i["id"] for i in response.json()]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.attendee_id in resp)
        self.assertFalse(self.admin_id in resp)

    def test_ViewItem_attendee_fail_organizer_admin(self):
        response = self.client.get(
            reverse("LC-wishlist"), HTTP_AUTHORIZATION=f"Token {self.attendee_token}"
        )
        resp = [i["id"] for i in response.json()]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.organizer_id in resp)
        self.assertFalse(self.admin_id in resp)

    def test_ViewItem_admin_fail_user_organizer(self):
        response = self.client.get(
            reverse("LC-wishlist"), HTTP_AUTHORIZATION=f"Token {self.admin_token}"
        )
        resp = [i["id"] for i in response.json()]
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
