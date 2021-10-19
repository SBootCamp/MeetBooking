from datetime import datetime
import random
import pytz
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import datetime
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from .factories import UserFactory, CabinetFactory, EventFactory
from .models import Event, Cabinet


class BookingTests(APITestCase):
    def create_event_json(self, start_time: datetime, end_time: datetime, visitors=None) -> dict:
        if visitors is None:
            visitors = []
        event = {
            'title': 'tests',
            'start_time': start_time,
            'end_time': end_time,
            'owner': self.user.id,
            'cabinet': self.cabinet.id,
            'visitors': visitors,
        }
        return event

    def setUp(self):
        self.now = timezone.now()
        self.client = APIClient()
        self.cabinet = CabinetFactory()
        self.user = UserFactory()
        self.event = EventFactory()
        self.visitors = UserFactory().create_batch(5)
        print(self.visitors)
        self.user_token = Token.objects.create(user=self.user)

        self.events_detail_url = reverse(
            'events-detail', kwargs={
                'room_number': self.cabinet.room_number,
                'pk': self.event.id
            })
        self.events_list_url = reverse(
            'events-list', kwargs={
                'room_number': self.cabinet.room_number,
            })

    def test_failure_event_created(self):
        start_time = datetime(
            year=self.now.year,
            month=self.now.month,
            day=self.now.day + 1,
            hour=10, minute=0, tzinfo=pytz.UTC
        )
        end_time = datetime(
            year=self.now.year,
            month=self.now.month,
            day=self.now.day + 1,
            hour=13, minute=0, tzinfo=pytz.UTC
        )
        event = self.create_event_json(start_time, end_time)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.post(self.events_list_url, event, format='json')
        self.assertEqual(response.json(), ['Указанное время занято'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success_event_created(self):
        start_time = datetime(
            year=self.now.year,
            month=self.now.month,
            day=self.now.day + 1,
            hour=15, minute=0, tzinfo=pytz.UTC
        )
        end_time = datetime(
            year=self.now.year,
            month=self.now.month,
            day=self.now.day + 1,
            hour=17, minute=0, tzinfo=pytz.UTC
        )
        # visitors =
        event = self.create_event_json(start_time, end_time)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.post(self.events_list_url, event, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
