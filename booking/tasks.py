from zoneinfo import ZoneInfo

from django.template.loader import render_to_string
from django.core.mail import send_mass_mail, send_mail
from django.contrib.auth.models import User
from django.db.models import Prefetch

from django.conf import settings

from booking.celery import app
from datetime import timedelta
from django.utils import timezone
from booking.models import Event


# from booking.tasks import send_events_mail
@app.task
def send_events_mail():
    now_date = timezone.now()
    end = timezone.now() + timedelta(minutes=settings.STEP_TIME_MINUTES)

    event_list = Event.objects.prefetch_related(Prefetch('visitors', queryset=User.objects.only('email'))) \
        .filter(start_time__gt=now_date, start_time__lte=end) \
        .select_related('cabinet',
                        'owner',
                        'cabinet')

    print(event_list)
    for event in event_list:
        # email_list = list(event.visitors.values_list('email', flat=True))
        # message = ('Напоминание о мероприятии',
        #            render_to_string('visitors_message.html'),
        #
        #            settings.EMAIL_HOST_USER,
        #            email_list)
        #
        # send_mass_mail((message,))

        owner_message = render_to_string(
            'owner_message.html',
            {
                'event_start_time': event.start_time,
                'event_end_time': event.end_time,
                'event_title': event.title,
                'event_cabinet': event.cabinet,
                'event_cabinet_floor': event.cabinet.floor,
            }
        )

        send_mail(
            'Напоминание о начале мероприятия',
            'Через 30 минут начало мероприятия',
            settings.EMAIL_HOST_USER,
            [event.owner.email],
            html_message=owner_message,
        )
