import datetime
import json
from calendar import monthrange


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
DATES = create_choice_date(2021, 9)
TIMES_CHOICES = tuple([(time, time) for time in TIMES])
DATES_CHOICES = tuple([(date, date) for date in DATES])


def create_time_list(events: list, date: datetime.date):
    time_list = []
    for time in TIMES:
        time_dict = {'time': time, 'event': None}
        for event in events:
            if event['start_time'].date() == date and event['start_time'].time() <= time <= event['end_time'].time():
                time_dict['event'] = event
        time_list.append(time_dict)
    return time_list


def create_schedule(events):
    schedule = [{str(date): create_time_list(list(events), date)} for date in DATES]
    return schedule
