from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils.datetime_safe import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Cabinet(models.Model):
    # photo = models.ImageField('Фото кабинета', upload_to='static/')
    place_count = models.IntegerField('Всего мест')
    projector = models.BooleanField('Наличие проектора')
    tv = models.BooleanField('ТВ')
    floor = models.IntegerField('Этаж')
    room_number = models.IntegerField('Номер кабинета', unique=True)

    def __str__(self):
        return str(self.room_number)


class Event(models.Model):
    title = models.CharField('Название мероприятия', max_length=250)
    date = models.DateField('Дата мероприятия')
    start_time = models.TimeField('Время начала мероприятия')
    end_time = models.TimeField('Время окончания мероприятия')
    cabinet = models.ForeignKey(
        Cabinet,
        on_delete=models.PROTECT,
        related_name='event_cabinet',
        verbose_name='Номер кабинета'
    )
    visitors = models.ManyToManyField(
        User,
        verbose_name='Посетители',
        related_name='event_visitors',
        blank=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Организатор',
        related_name='event_sponsor'
    )

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('Время окончания мероприятия должно быть меньше времени начала мероприятия')

        elif Event.objects.filter(
                Q(start_time__lte=self.start_time,
                  end_time__gte=self.start_time, cabinet=self.cabinet,
                  date=self.date) |
                Q(start_time__lte=self.end_time, end_time__gte=self.end_time, cabinet=self.cabinet,
                  date=self.date) |
                Q(start_time__gte=self.start_time, end_time__lte=self.end_time, cabinet=self.cabinet,
                  date=self.date)).exists():
            raise ValidationError('Указанное время занято')

        elif self.date < datetime.now().date() \
                and self.start_time < datetime.now().time() \
                or self.date < datetime.now().date():
            raise ValidationError('Запись на указанное время завершена')


    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ['cabinet', 'date', 'start_time', 'end_time']

    def duration(self):
        pass

    def __str__(self):
        return self.title
