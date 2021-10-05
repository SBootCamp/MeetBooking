import calendar
import copy
import datetime
import typing
import pytz
from django.utils import timezone

from MeetBooking.settings import START_TIME, END_TIME, STEP_TIME_MINUTES


def create_time_list(start_time: int, end_time: int, step_time_minutes: int) -> typing.List[typing.Tuple[int, int]]:
    start_time_second = start_time * 3600
    end_time_second = end_time * 3600
    step_time_second = step_time_minutes * 60
    return [(sec // 3600, sec % 3600 // 60) for sec in range(start_time_second, end_time_second + 1, step_time_second)]


def create_date_list(year: int, month: int) -> typing.List[datetime.datetime]:
    return [datetime.datetime(year=year, month=month, day=day, tzinfo=pytz.UTC)
            for day in range(1, calendar.monthrange(year, month)[1] + 1)]


def create_datetime_dict(dates: list, times: list) -> typing.Dict[str, typing.Dict[str, None]]:
    return {str(date.date()): {str(datetime.time(*time)): None for time in times} for date in dates}


def create_datetime_list() -> typing.List[datetime.datetime]:
    dates = create_date_list(timezone.now().year, timezone.now().month)
    times = create_time_list(START_TIME, END_TIME, STEP_TIME_MINUTES)
    return [date + datetime.timedelta(hours=hours, minutes=minutes) for date in dates for hours, minutes in times]


def create_schedule(events: typing.List[dict]) -> typing.Dict[str, typing.Dict[str, None or dict]]:
    times = create_time_list(START_TIME, END_TIME, STEP_TIME_MINUTES)
    dates = create_date_list(timezone.now().year, timezone.now().month)
    date_times_dict = create_datetime_dict(dates, times)
    schedule = copy.deepcopy(date_times_dict)
    for event in events:
        start_time = event['start_time']
        end_time = event['end_time']
        while start_time != end_time:
            date = str(start_time.date())
            time = str(start_time.time())
            schedule[date][time] = event
            start_time += datetime.timedelta(minutes=STEP_TIME_MINUTES)
    return schedule
