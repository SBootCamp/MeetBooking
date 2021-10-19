from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from .factories import UserFactory, CabinetFactory, EventFactory, get_datetime, create_event_json


class BookingTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.cabinet = CabinetFactory()
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.event = EventFactory(cabinet=self.cabinet, owner=self.user_1)
        self.visitors = [UserFactory().id for _ in range(10)]
        self.user_token_1 = Token.objects.create(user=self.user_1)
        self.user_token_2 = Token.objects.create(user=self.user_2)
        self.events_detail_url = reverse(
            'events-detail', kwargs={
                'name': self.cabinet.name,
                'pk': self.event.id
            })
        self.events_list_url = reverse(
            'events-list', kwargs={
                'name': self.cabinet.name,
            })

    def test_failure_event_created(self):
        start_time = get_datetime(hour=10)
        end_time = get_datetime(hour=13)
        event = create_event_json(start_time, end_time, self.cabinet, self.user_1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token_1.key)
        response = self.client.post(self.events_list_url, event, format='json')
        self.assertEqual(response.json(), ['Указанное время занято'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success_event_created(self):
        start_time = get_datetime(hour=15)
        end_time = get_datetime(hour=17)
        event = create_event_json(start_time, end_time, self.cabinet, self.user_1, self.visitors)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token_1.key)
        response = self.client.post(self.events_list_url, event, format='json')
        self.assertEqual(response.json().get('visitors'), self.visitors)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_success_patch_event(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token_1.key)
        response = self.client.patch(self.events_detail_url, {'title': 'rename'}, format='json')
        self.assertEqual(response.json().get('title'), 'rename')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_failure_patch_event(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token_2.key)
        response = self.client.patch(self.events_detail_url, {'title': 'rename'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_success_delete_event(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token_1.key)
        response = self.client.delete(self.events_detail_url, self.event.id, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_failure_delete_event(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token_2.key)
        response = self.client.delete(self.events_detail_url, self.event.id, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
