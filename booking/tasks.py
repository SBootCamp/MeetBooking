from django.core.mail import send_mail
from booking.celery import app
from booking.models import Event
from datetime import datetime, timedelta


@app.task
def send_spam_email():
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    list = Event.objects.order_by('start_time')
    nearest_event_time = getattr(list[0], 'start_time')
    print(nearest_event_time.strftime('%Y-%m-%d %H:%M'))
    print(now_time)
    print('------')
    time_to_send = nearest_event_time - timedelta(minutes=30)
    print(time_to_send.strftime('%Y-%m-%d %H:%M'))
    if time_to_send.strftime('%Y-%m-%d %H:%M') == nearest_event_time.strftime('%Y-%m-%d %H:%M'):
        send_mail(
            'Напоминание о мероприятии',
            '',
            'mbannakov13@gmail.com',
            [mail.email],
            fail_silently=False,
        )

#celery -A MeetBooking worker -l info
#celery -A MeetBooking beat -l info
#from booking.tasks import send_spam_email
