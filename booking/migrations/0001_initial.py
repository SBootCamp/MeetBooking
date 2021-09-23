# Generated by Django 3.2.7 on 2021-09-23 21:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_places', models.IntegerField(verbose_name='Всего мест')),
                ('projector', models.BooleanField(verbose_name='Наличие проектора')),
                ('floor', models.IntegerField(verbose_name='Этаж')),
                ('room_number', models.IntegerField(unique=True, verbose_name='Номер кабинета')),
            ],
        ),
        migrations.CreateModel(
            name='DateBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата бронирования')),
            ],
        ),
        migrations.CreateModel(
            name='TimeBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(verbose_name='Время бронирования')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Название мероприятия')),
                ('completed', models.BooleanField(verbose_name='Completed')),
                ('technical_work', models.BooleanField(blank=True, default=False, null=True, verbose_name='Технические работы')),
                ('cabinet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='event_cabinet', to='booking.cabinet', verbose_name='Кабинет')),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_date', to='booking.datebooking', verbose_name='Дата')),
                ('end_time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_end_time', to='booking.timebooking', verbose_name='Время окончания мероприятия')),
                ('sponsor', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='event_sponsor', to=settings.AUTH_USER_MODEL, verbose_name='Организатор')),
                ('start_time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_start_time', to='booking.timebooking', verbose_name='Время начала мероприятия')),
                ('visitors', models.ManyToManyField(blank=True, null=True, related_name='event_visitors', to=settings.AUTH_USER_MODEL, verbose_name='Посетители')),
            ],
        ),
    ]