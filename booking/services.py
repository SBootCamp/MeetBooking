import calendar
import copy
import datetime
import typing
import pytz
from django.utils import timezone

from MeetBooking.settings import START_TIME, END_TIME, STEP_TIME

NOW = timezone.now()
YEAR_NOW = NOW.year
MONTH_NOW = NOW.month


def create_time_list(start_time: int, end_time: int, step_time: int) -> typing.List[typing.Tuple[int, int]]:
    cut = 60 // step_time - 1
    return [(hour, minute) for hour in range(start_time, end_time + 1)
            for minute in range(0, 60, step_time)][:-cut]


def create_date_list(year: int, month: int) -> typing.List[datetime.datetime]:
    return [datetime.datetime(year=year, month=month, day=day, tzinfo=pytz.UTC)
            for day in range(1, calendar.monthrange(year, month)[1] + 1)]


def create_datetime_dict(dates: list, times: list) -> typing.Dict[str, typing.Dict[str, None]]:
    return {str(date.date()): {str(datetime.time(*time)): None for time in times} for date in dates}


def create_datetime_list(dates: list, times: list) -> typing.List[datetime.datetime]:
    return [date + datetime.timedelta(hours=time[0], minutes=time[1]) for date in dates for time in times]


TIMES = create_time_list(START_TIME, END_TIME, STEP_TIME)
DATES = create_date_list(YEAR_NOW, MONTH_NOW)
DATE_TIMES_DICT = create_datetime_dict(DATES, TIMES)
DATE_TIMES_LIST = create_datetime_list(DATES, TIMES)


def create_schedule(events: typing.List[dict]) -> typing.Dict[str, typing.Dict[str, None or dict]]:
    schedule = copy.deepcopy(DATE_TIMES_DICT)
    for event in events:
        start_time = event['start_time']
        end_time = event['end_time']
        while start_time != end_time:
            date = str(start_time.date())
            time = str(start_time.time())
            schedule[date][time] = event
            start_time += datetime.timedelta(minutes=STEP_TIME)
    return schedule
