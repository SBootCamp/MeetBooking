from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateTimeRangeField, RangeOperators, RangeBoundary
from django.db.models import Q, Func
from django.utils.datetime_safe import datetime as dt


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


class TsTzRange(Func):
    function = 'TSTZRANGE'
    output_field = DateTimeRangeField()


class Event(models.Model):
    title = models.CharField(verbose_name='Название мероприятия', max_length=250, default='')
    start_time = models.DateTimeField(verbose_name='Время начала мероприятия')
    end_time = models.DateTimeField(verbose_name='Время окончания мероприятия')
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

    # TODO:add functionality
    def duration(self):
        pass

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        constraints = [
            ExclusionConstraint(
                name='overlap_booking',
                expressions=(
                    (TsTzRange('start_time', 'end_time', RangeBoundary()), RangeOperators.OVERLAPS),
                    ('cabinet', RangeOperators.EQUAL),
                ),
            ),
        ]
