from django.contrib.auth.models import User
from django.db import models


class Cabinet(models.Model):
    photo = models.ImageField('Фото кабинета', upload_to='static/' )
    number_places = models.IntegerField('Всего мест')
    projector = models.BooleanField('Наличие проектора')
    floor = models.IntegerField('Этаж')
    room_number = models.IntegerField('Номер кабинета')

    def __str__(self):
        return self.room_number

class Event(models.Model):
    title = models.CharField('Название мероприятия', max_length=250)
    date = models.DateField('Дата проведения мероприятия')
    start_time = models.TimeField('Время начала мероприятия')
    end_time = models.TimeField('Время окончания мероприятия')
    completed = models.BooleanField('Completed')
    visitors = models.ManyToManyField(
        User,
        verbose_name='Посетители',
        related_name='event_visitors',
        blank=True, null=True
    )
    sponsor = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Организатор',
        related_name='event_sponsor'
    )
    cabinet = models.ForeignKey(
        Cabinet,
        on_delete=models.CASCADE,
        related_name='event_cabinet',
        verbose_name='Кабинет'
    )

    def __str__(self):
        return self.title


