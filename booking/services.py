from calendar import monthrange
import datetime
from collections import OrderedDict

from django.db.models import Q

from .models import TimeBooking, DateBooking, Event

TIMES = ('09:00', '09:30', '10:00',
         '10:30', '11:00', '11:30',
         '12:00', '12:30', '13:00',
         '13:30', '14:00', '14:30',
         '15:00', '15:30', '16:00',
         '16:30', '17:00', '17:30',
         '18:00', '18:30', '19:00',
         '19:30', '20:00', '20:30',
         '21:00',
         )


def create_update_time():
    for time in TIMES:
        if not TimeBooking.objects.filter(time=time, ).exists():
            tm = TimeBooking.objects.create(time=time)
            tm.save()


def create_update_date():
    if not DateBooking.objects.filter(date=str(datetime.datetime.now().date())).exists():
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        dates = ['{:04d}-{:02d}-{:02d}'.format(datetime.datetime.now().year, month, day)
                 for day in range(1, monthrange(year, month)[1] + 1)]
        DateBooking.objects.all().delete()
        for date in dates:
            dt = DateBooking.objects.create(date=date)
            dt.save()
    create_update_time()


def booked_time(room_number):
    events = Event.objects.filter(
        cabinet__room_number=room_number
    ).prefetch_related('time').select_related('date')
    date_booking = {}
    for event in events:
        time_booking = list(event.time.all())
        time = date_booking.get(event.date)
        date_booking[event.date] = time + time_booking if time is not None else time_booking
    return date_booking

def schedule(room_number):


