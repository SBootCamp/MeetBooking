from datetime import datetime
import factory
import pytz
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils import timezone
from factory import fuzzy
from booking.models import Event, Cabinet


def get_datetime(hour):
    now = timezone.now()
    return datetime(year=now.year, month=now.month, day=now.day + 1, hour=hour, minute=0, tzinfo=pytz.UTC)


def create_event_json(start_time, end_time, cabinet, owner, visitors=None, title='test') -> dict:
    if visitors is None:
        visitors = []
    event = {
        'title': title,
        'start_time': start_time,
        'end_time': end_time,
        'owner': owner.id,
        'cabinet': cabinet.id,
        'visitors': visitors,
    }
    return event


class UserFactory(factory.django.DjangoModelFactory):
    last_name = factory.Faker('last_name')
    username = factory.Faker('email')
    password = factory.LazyFunction(lambda: make_password('12345678'))
    is_active = True

    class Meta:
        model = User


class CabinetFactory(factory.django.DjangoModelFactory):
    place_count = '30'
    projector = True
    tv = True
    floor = 5
    room_number = 2
    name = '2'

    class Meta:
        model = Cabinet


class EventFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('first_name'),
    start_time = factory.LazyFunction(lambda: get_datetime(12))
    end_time = factory.LazyFunction(lambda: get_datetime(15))
    owner = factory.SubFactory(UserFactory)
    cabinet = factory.SubFactory(CabinetFactory)

    class Meta:
        model = Event