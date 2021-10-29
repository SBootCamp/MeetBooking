import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meet_booking.settings')

app = Celery('booking')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-email': {
        'task': 'booking.tasks.send_events_mail',
        'schedule': crontab(minute=settings.CELERY_SEND_MAIL_SCHEDULE)
    }
}
