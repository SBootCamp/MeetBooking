from datetime import datetime
import factory
import pytz
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils import timezone

from booking.models import Event, Cabinet


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    last_name = factory.Faker('last_name')
    username = factory.Faker('email')
    password = factory.LazyFunction(lambda: make_password('12345678'))
    is_active = True

class CabinetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cabinet

    place_count = '30'
    projector = True
    tv = True
    floor = 5
    room_number = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: 'room%d' % n)


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event
    title = factory.Faker('sentence', nb_words=4),
    start_time = datetime(
        year=timezone.now.year,
        month=now.month,
        day=now.day + 1,
        hour=12, minute=0, tzinfo=pytz.UTC
    ),
    end_time = datetime(
        year=now.year,
        month=now.month,
        day=now.day + 1,
        hour=15, minute=0, tzinfo=pytz.UTC
    ),
    owner = factory.SubFactory(UserFactory)
    cabinet = factory.SubFactory(CabinetFactory)



