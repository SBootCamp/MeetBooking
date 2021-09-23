from django.contrib.auth.models import User
from django.db import models


class Cabinet(models.Model):
    # photo = models.ImageField('Фото кабинета', upload_to='static/')
    number_places = models.IntegerField('Всего мест')
    projector = models.BooleanField('Наличие проектора')
    floor = models.IntegerField('Этаж')
    room_number = models.IntegerField('Номер кабинета', unique=True)

    def __str__(self):
        return str(self.room_number)


class DateBooking(models.Model):
    date = models.DateField('Дата бронирования')

    def __str__(self):
        return f"Date {self.date}"


class TimeBooking(models.Model):
    time = models.TimeField('Время бронирования')

    def __str__(self):
        return f"Time {self.time}"


class Event(models.Model):
    title = models.CharField('Название мероприятия', max_length=250)
    date = models.ForeignKey(
        DateBooking,
        on_delete=models.CASCADE,
        related_name='event_date',
        verbose_name='Дата'
    )
    time = models.ManyToManyField(
        TimeBooking,
        related_name='event_time',
        verbose_name='Время мероприятия'
    )
    cabinet = models.ForeignKey(
        Cabinet,
        on_delete=models.PROTECT,
        related_name='event_cabinet',
        verbose_name='Кабинет'
    )
    completed = models.BooleanField('Completed')
    visitors = models.ManyToManyField(
        User,
        verbose_name='Посетители',
        related_name='event_visitors',
        blank=True, null=True,
    )
    sponsor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Организатор',
        related_name='event_sponsor',
        blank=True,
    )
    technical_work = models.BooleanField('Технические работы', default=False, blank=True, null=True)

    def __str__(self):
        return self.title
