from django.core.mail import send_mail
from booking.celery import app


@app.task
def send_spam_email():
    send_mail(
        'Тест',
        'Тест',
        'mbannakov13@gmail.com',
        ['mbannakov14@yahoo.com'],
        fail_silently=False,
    )

#celery -A MeetBooking worker -l info
#celery -A MeetBooking beat -l info