from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.datetime_safe import datetime


class Cabinet(models.Model):
    # photo = models.ImageField('Фото кабинета', upload_to='static/')
    place_count = models.IntegerField(verbose_name='Всего мест', default=0)
    projector = models.BooleanField(verbose_name='Наличие проектора', default=False)
    tv = models.BooleanField(verbose_name='ТВ', default=False)
    floor = models.IntegerField(verbose_name='Этаж')
    room_number = models.IntegerField(verbose_name='Номер кабинета')

    def __str__(self):
        return str(self.room_number)

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'


class Event(models.Model):
    title = models.CharField(verbose_name='Название мероприятия', max_length=250, default='')
    date = models.DateField(verbose_name='Дата мероприятия')
    start_time = models.TimeField(verbose_name='Время начала мероприятия')
    end_time = models.TimeField(verbose_name='Время окончания мероприятия')
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
        related_name='event_owner'
    )

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('Время окончания мероприятия должно быть больше времени начала мероприятия')

        elif Event.objects.filter(
                Q(start_time__lte=self.start_time,
                  end_time__gt=self.start_time,
                  cabinet=self.cabinet,
                  date=self.date) |
                Q(start_time__lt=self.end_time,
                  end_time__gte=self.end_time,
                  cabinet=self.cabinet,
                  date=self.date) |
                Q(start_time__gte=self.start_time,
                  end_time__lte=self.end_time,
                  cabinet=self.cabinet,
                  date=self.date)
        ).exclude(id=self.id).exists():
            raise ValidationError('Указанное время занято')

        elif self.date <= datetime.now().date() \
                and self.start_time < datetime.now().time() \
                and self.end_time < datetime.now().time():
            raise ValidationError('Запись на указанное время завершена')

    # TODO:add functionality
    def duration(self):
        pass

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
