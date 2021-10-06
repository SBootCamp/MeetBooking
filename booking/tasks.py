from zoneinfo import ZoneInfo

from django.core.mail import send_mass_mail, send_mail
from django.contrib.auth.models import User
from django.db.models import Prefetch

from MeetBooking.settings import EMAIL_HOST_USER
from booking.celery import app
from datetime import timedelta
from django.utils import timezone

from booking.models import Event


@app.task
def send_events_mail():
    now_date = timezone.now()
    end = timezone.now() + timedelta(minutes=30)

    event_list = Event.objects.prefetch_related(Prefetch('visitors', queryset=User.objects.only('email'))) \
        .filter(start_time__gte=now_date, start_time__lte=end) \
        .only('visitors')

    for event in event_list:
        email_dict = event.visitors.values('email')
        email_list = [email.get('email') for email in email_dict]

        message = ('Напоминание о мероприятии',
                   f"Здравствуйте, мероприятие '{event.title}' \
                   будет длиться с {event.start_time.astimezone(tz=ZoneInfo('Europe/Moscow'))} \
                    до {event.end_time.astimezone(tz=ZoneInfo('Europe/Moscow'))}, \
                   в {event.cabinet} кабинете, на {event.cabinet.floor} этаже",

                   EMAIL_HOST_USER,
                   email_list)

        send_mass_mail((message,))

        send_mail(
            'Напоминание о мероприятии для руководителя',
            f"Здравствуйте, мероприятие '{event.title}' \
            будет длиться с {event.start_time.astimezone(tz=ZoneInfo('Europe/Moscow'))} \
            до {event.end_time.astimezone(tz=ZoneInfo('Europe/Moscow'))}, \
            в {event.cabinet} кабинете, на {event.cabinet.floor} этаже",

            EMAIL_HOST_USER,
            [event.owner.email],
        )
