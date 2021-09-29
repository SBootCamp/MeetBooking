from django.core.mail import send_mail
from booking.celery import app
from booking.models import Event
from datetime import datetime


@app.task
def send_spam_email():
    #now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #list = Event.objects.values_list('start_time')
    #print(list[0])


#celery -A MeetBooking worker -l info
#celery -A MeetBooking beat -l info
#from booking.tasks import send_spam_email
