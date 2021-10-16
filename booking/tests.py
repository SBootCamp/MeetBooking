import pytz
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import datetime
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from .models import Event, Cabinet


class BookingTests(APITestCase):
    def create_event_json(self, start_time_hour, end_time_hour):
        event = {
            'title': 'tests',
            'start_time': datetime(
                year=timezone.now().year,
                month=timezone.now().month,
                day=timezone.now().day + 1,
                hour=start_time_hour, minute=0, tzinfo=pytz.UTC
            ),
            'end_time': datetime(
                year=timezone.now().year,
                month=timezone.now().month,
                day=timezone.now().day + 1,
                hour=end_time_hour, minute=0, tzinfo=pytz.UTC
            ),
            'owner': self.user.id,
            'cabinet': self.cabinet.id,
            'visitors': [],
        }
        return event

    def setUp(self):
        self.client = APIClient()
        self.cabinet = Cabinet.objects.create(floor=1, room_number=2)
        self.user = User.objects.create_user(
            username='user_test',
            email='test@mail.ru',
            password='12345678'
        )
        self.user_token = Token.objects.create(user=self.user)
        self.event = Event.objects.create(
            title='tests',
            start_time=datetime(
                year=timezone.now().year,
                month=timezone.now().month,
                day=timezone.now().day + 1,
                hour=12, minute=0, tzinfo=pytz.UTC
            ),
            end_time=datetime(
                year=timezone.now().year,
                month=timezone.now().month,
                day=timezone.now().day + 1,
                hour=15, minute=0, tzinfo=pytz.UTC
            ),
            owner=self.user,
            cabinet=self.cabinet
        )
        self.events_detail_url = reverse(
            'events-detail', kwargs={
                'room_number': self.cabinet.room_number,
                'pk': self.event.id
            })
        self.events_list_url = reverse(
            'events-list', kwargs={
                'room_number': self.cabinet.room_number,
            })

    def test_intersection_time_events_variant_one(self):
        event = self.create_event_json(start_time_hour=10, end_time_hour=13)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.post(self.events_list_url, event, format='json')
        self.assertEqual(response.json(), ['Указанное время занято'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_intersection_time_events_variant_two(self):
        event = self.create_event_json(start_time_hour=13, end_time_hour=17)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.post(self.events_list_url, event, format='json')
        self.assertEqual(response.json(), ['Указанное время занято'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_intersection_time_events_variant_three(self):
        event = self.create_event_json(start_time_hour=13, end_time_hour=14)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.post(self.events_list_url, event, format='json')
        self.assertEqual(response.json(), ['Указанное время занято'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_intersection_time_events_variant_four(self):
        event = self.create_event_json(start_time_hour=10, end_time_hour=12)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.post(self.events_list_url, event, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_intersection_time_events_variant_five(self):
        event = self.create_event_json(start_time_hour=15, end_time_hour=17)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.post(self.events_list_url, event, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
