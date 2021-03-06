# Generated by Django 3.2.7 on 2021-10-15 16:13
from django.contrib.postgres.operations import BtreeGistExtension
import booking.contrib.postgres.functions
from django.conf import settings
import django.contrib.postgres.constraints
import django.contrib.postgres.fields.ranges
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        BtreeGistExtension(),
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_count', models.IntegerField(default=0, verbose_name='Всего мест')),
                ('projector', models.BooleanField(default=False, verbose_name='Наличие проектора')),
                ('tv', models.BooleanField(default=False, verbose_name='Наличие ТВ')),
                ('floor', models.IntegerField(verbose_name='Этаж')),
                ('room_number', models.IntegerField(verbose_name='Номер кабинета')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Наименование кабинета')),
            ],
            options={
                'verbose_name': 'Кабинет',
                'verbose_name_plural': 'Кабинеты',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=250, verbose_name='Название мероприятия')),
                ('start_time', models.DateTimeField(verbose_name='Время начала мероприятия')),
                ('end_time', models.DateTimeField(verbose_name='Время окончания мероприятия')),
                ('cabinet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='event_cabinet', to='booking.cabinet', verbose_name='Номер кабинета')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='event_owner', to=settings.AUTH_USER_MODEL, verbose_name='Организатор')),
                ('visitors', models.ManyToManyField(blank=True, related_name='event_visitors', to=settings.AUTH_USER_MODEL, verbose_name='Посетители')),
            ],
            options={
                'verbose_name': 'Мероприятие',
                'verbose_name_plural': 'Мероприятия',
            },
        ),
        migrations.AddConstraint(
            model_name='event',
            constraint=django.contrib.postgres.constraints.ExclusionConstraint(expressions=((booking.contrib.postgres.functions.TsTzRange('start_time', 'end_time', django.contrib.postgres.fields.ranges.RangeBoundary()), '&&'), ('cabinet', '=')), name='overlap_booking'),
        ),
        migrations.AddConstraint(
            model_name='event',
            constraint=models.CheckConstraint(check=models.Q(('start_time__lt', django.db.models.expressions.F('end_time'))), name='check_datetime'),
        ),
    ]
