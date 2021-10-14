import calendar
import copy
import datetime
from typing import List, Any
import pytz
from django.utils import timezone

from MeetBooking.settings import START_TIME, END_TIME, STEP_TIME_MINUTES


def create_time_list(start_time: int, end_time: int, step_time_minutes: int) -> list[tuple[int, int]]:
    start_time_second = start_time * 3600
    end_time_second = end_time * 3600
    step_time_second = step_time_minutes * 60
    return [(sec // 3600, sec % 3600 // 60) for sec in range(start_time_second, end_time_second + 1, step_time_second)]


def create_date_list(year: int, month: int) -> list[datetime.datetime]:
    return [datetime.datetime(year=year, month=month, day=day, tzinfo=pytz.UTC)
            for day in range(1, calendar.monthrange(year, month)[1] + 1)]


def get_times_and_dates() -> tuple[list, list]:
    dates = create_date_list(timezone.now().year, timezone.now().month)
    times = create_time_list(START_TIME, END_TIME, STEP_TIME_MINUTES)
    return times, dates


def create_datetime_dict(dates: list, times: list) -> dict[str, dict[str, None]]:
    return {str(date.date()): {str(datetime.time(*time)): None for time in times} for date in dates}


def create_datetime_list() -> List[datetime.datetime]:
    times, dates = get_times_and_dates()
    return [date + datetime.timedelta(hours=hours, minutes=minutes) for date in dates for hours, minutes in times]


def create_date_choices() -> tuple[tuple[Any, Any]]:
    times, dates = get_times_and_dates()
    date_choices = tuple([(date.date(), date.date()) for date in dates])
    return date_choices


def create_time_choices() -> tuple[tuple[datetime.time, datetime.time]]:
    times, dates = get_times_and_dates()
    time_choices = tuple([(datetime.time(*time), datetime.time(*time)) for time in times])
    return time_choices


def create_schedule(events: list[dict]) -> list[dict[str, dict[str, None or dict]]]:
    times, dates = get_times_and_dates()
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
    return [{key: value} for key, value in schedule.items()]
