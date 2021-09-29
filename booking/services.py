import datetime
from calendar import monthrange
import random
import pytz

from booking.models import Event


def create_choice_time(start: int, end: int, delta: int):
    """
    :param start: int
    :param end: int
    :param delta: minute
    :return: list times
    """
    cut = 60 // delta - 1
    return [datetime.time(hour=i, minute=j) for i in range(start, end + 1) for j in range(0, 60, delta)][:-cut]


def create_choice_date(year: int, month: int):
    return [datetime.date(year=year, month=month, day=day) for day in range(1, monthrange(2021, 9)[1] + 1)]


TIMES = create_choice_time(9, 21, 30)
DATES = create_choice_date(2021, 10)
TIMES_CHOICES = tuple([(time, time) for time in TIMES])
DATES_CHOICES = tuple([(date, date) for date in DATES])


def create_test_event():
    for i in range(0, 5000):
        delta = (0, 30)
        day = random.randint(1, 31)
        date_time_start = datetime.datetime(
            year=2021, month=10,
            day=day, hour=random.randint(9, 21),
            minute=random.choice(delta),
            tzinfo=pytz.UTC,
        )
        date_time_end = datetime.datetime(
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
                cabinet_id=1
            )
            print(f'Good {i}')
        except:
            continue


def update_time_dict(time_dict, time, date, events):
    for event in events:
        if event['start_time'].date() == date:
            if event['start_time'].time() <= time <= event['end_time'].time():
                time_dict[f'{time}'] = event
    return time_dict


def create_time_list(events: list, date: datetime.date):
    return [update_time_dict({f'{time}': None}, time, date, events) for time in TIMES]


def create_schedule(events):
    return [{str(date): create_time_list(events, date)} for date in DATES]
