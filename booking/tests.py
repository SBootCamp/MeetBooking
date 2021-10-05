from datetime import datetime
import random
import pytz
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from booking.models import Event


def create_test_event(cabinet):
    for i in range(0, 5000):
        delta = (0, 30)
        day = random.randint(1, 31)
        date_time_start = datetime(
            year=2021, month=10,
            day=day, hour=random.randint(9, 21),
            minute=random.choice(delta),
            tzinfo=pytz.UTC,
        )
        date_time_end = datetime(
            year=2021, month=10,
            day=day, hour=random.randint(9, 21),
            minute=random.choice(delta),
            tzinfo=pytz.UTC,
        )
        try:
            Event.objects.create(
                title=f'test {i}',
                start_time=date_time_start,
                end_time=date_time_end,
                owner_id=1,
                cabinet=cabinet
            )
            print(f'Good {i}')
        except (IntegrityError, ValidationError):
            continue


USERNAME = [
    'Johnny Taylor', 'Mark Baldwin', 'Leon Fitzgerald', 'Calvin Reed', 'Dale Barrett', 'Brian Smith',
    'Robert Vasquez', 'James Garcia', 'Marvin Schmidt', 'Steven Moore', 'Keith Medina', 'Christopher Martinez',
    'Jason Poole', 'Stephen James', 'Pedro Williams', 'DanielBrown', 'Elmer Peters', 'Charles Davidson', 'Marc Powell',
    'Charles Anderson', 'John Ellis', 'Kenneth Mitchell', 'Richard Murray', 'Charles Mason', 'Larry Hill',
    'Matthew Vega', 'Kenneth Romero', 'Leon Francis', 'Victor Crawford', 'Richard Ross', 'Edward Carr', 'Jeffrey Day',
    'Frank Lopez', 'Harold Thompson', 'Thomas Barnes', 'Ramon Sanchez', 'Hector Stokes', 'Dale Williams',
    'Andrew Drake', 'James Stewart', 'Mike Newton', 'Chester Blair', 'Larry Barrett', 'Henry Watson', 'Robert Wright',
    'Donald Martin', 'Robert Hicks', 'Donald Padilla', 'Jesse Morrison', 'Greg Glover'
]


def create_test_user():
    User.objects.bulk_create([
        User(
            username=name,
            email='USER@email.ru',
            password=make_password('12345678'),
            is_active=True,
        ) for name in USERNAME
    ])
