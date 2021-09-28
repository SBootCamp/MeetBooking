import datetime
from calendar import monthrange


def create_choice_time(start, end, delta):
    cut = 60 // delta-1
    return [datetime.time(hour=i, minute=j) for i in range(start, end + 1) for j in range(0, 60, delta)][:-cut]


TIMES = create_choice_time(9, 21, 30)
DATES = ['{:04d}-{:02d}-{:02d}'.format(2021, 9, day, ) for day in range(1, monthrange(2021, 9)[1] + 1)]
TIMES_CHOICES = tuple([(time, time) for time in TIMES])
DATES_CHOICES = tuple([(date, date) for date in DATES])