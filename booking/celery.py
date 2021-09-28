import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MeetBooking.settings')

app = Celery('booking')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-spam': {
        'task': 'booking.tasks.send_spam_email',
        'schedule': crontab(minute='*/1')
    }
}