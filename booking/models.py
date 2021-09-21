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

class DateRecord(models.Model):
    date = models.DateField('Дата бронирования')

    def __str__(self):
        return f"Date {self.date}"


class TimeRecord(models.Model):
    time = models.TimeField('Время бронирования')

    def __str__(self):
        return f"Time {self.time}"

class TechnicalWork(models.Model):
    title = models.CharField('Название тех.работ', max_length=250)
    date = models.OneToOneField(
        DateRecord,
        on_delete=models.SET_NULL,
        related_name='technical_date',
        verbose_name='Дата проведения мероприятия'
    )
    time = models.ManyToManyField(
        TimeRecord,
        verbose_name='Время проведения мероприятия',
        related_name='technical_time'
    )
    cabinet = models.ForeignKey(
        Cabinet,
        on_delete=models.CASCADE,
        related_name='technical_cabinet',
        verbose_name='Кабинет'
    )

    def __str__(self):
        return self.title

class Event(TechnicalWork):
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

    def __str__(self):
        return self.title


