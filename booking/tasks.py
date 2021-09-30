from django.core.mail import send_mass_mail
from django.contrib.auth.models import User

from MeetBooking.settings import EMAIL_HOST_USER
from booking.celery import app
from booking.models import Event
from datetime import datetime, timedelta
from django.utils import timezone

@app.task
def send_spam_email():
    now_date = timezone.now()
    end = timezone.now() + timedelta(minutes=32)

    user_list = User.objects.prefetch_related('event_visitors')\
        .filter(event_visitors__start_time__gte=now_date, event_visitors__start_time__lte=end)\
        .values('email', 'event_visitors__start_time')

    email_list = [user.get('email') for user in user_list]
    event_start = user_list[0].get('event_visitors__start_time')

    if user_list:
        message = ('Напоминание о мероприятии',
                   f'Ваше мероприятие начнется через 30 минут, {event_start}',
                   EMAIL_HOST_USER,
                   email_list)
        send_mass_mail((message,), fail_silently=False)

#celery -A booking worker -l info
#celery -A booking beat -l info
#from booking.tasks import send_spam_email