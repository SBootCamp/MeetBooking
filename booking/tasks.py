from zoneinfo import ZoneInfo

from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.template.loader import render_to_string
from django.core.mail import send_mail

from django.conf import settings

from booking.celery import app
from datetime import timedelta
from django.utils import timezone
from booking.models import Event

@app.task
def send_events_mail():
    now_date = timezone.now()
    end = timezone.now() + timedelta(minutes=settings.STEP_TIME_MINUTES)

    event_list = Event.objects.prefetch_related(Prefetch('visitors', queryset=User.objects.only('email', 'username')))\
        .filter(start_time__gt=now_date, start_time__lte=end) \
        .select_related('cabinet',
                        'owner', )

    for event in event_list:
        email_list = [visitors.email for visitors in event.visitors.all()]
        username_list = [visitors.username for visitors in event.visitors.all()]
        visitors_message = render_to_string(
            'visitors_message.html',
            {
                'event_start_time': event.start_time,
                'event_end_time': event.end_time,
                'event_title': event.title,
                'event_cabinet': event.cabinet,
                'event_cabinet_floor': event.cabinet.floor,
            }
        )

        # Письма для посетителей мероприятия
        send_mail('Напоминание о начале мероприятия',
                  'Через 30 минут начало мероприятия',
                  settings.EMAIL_HOST_USER,
                  email_list,
                  html_message=visitors_message)

        owner_message = render_to_string(
            'owner_message.html',
            {
                'user_name_list': username_list,
                'event_start_time': event.start_time.astimezone(tz=ZoneInfo('Europe/Moscow')),
                'event_end_time': event.end_time.astimezone(tz=ZoneInfo('Europe/Moscow')),
                'event_title': event.title,
                'event_cabinet': event.cabinet,
                'event_cabinet_floor': event.cabinet.floor,
            }
        )

        # Письмо для руководителя
        send_mail(
            'Вы создали мероприятие которое начнется через 30 минут',
            'Через 30 минут начало мероприятия',
            settings.EMAIL_HOST_USER,
            [event.owner.email],
            html_message=owner_message,
        )
