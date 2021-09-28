from django.contrib.auth.models import User
from django.core.mail import send_mail
from .celery import app





@app.task
def send_spam_email():
    for user in User.objects.all():
            send_mail(
                'Тест',
                'Тест',
                'test-infomaxim@yandex.ru',
                [user.email],
                fail_silently=False,
            )

#python3 manage.py runserver
#celery -A app worker -l info
#celery -A app beat -l info