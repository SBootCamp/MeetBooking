from calendar import monthrange

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from booking.models import Event, Cabinet

TIMES = [
    '09:00', '09:30', '10:00', '10:30', '11:00',
    '11:30', '12:00', '12:30', '13:00', '13:30',
    '14:00', '14:30', '15:00', '15:30', '16:00',
    '16:30', '17:00', '17:30', '18:00', '18:30',
    '19:00', '19:30', '20:00', '20:30', '21:00',
]
DATES = ['{:04d}-{:02d}-{:02d}'.format(2021, 9, day) for day in range(1, monthrange(2021, 9)[1] + 1)]
blank_choice = (('', '----'),)
TIMES_CHOICES = blank_choice + tuple([(time, time) for time in TIMES])
DATES_CHOICES = blank_choice + tuple([(date, date) for date in DATES])


class BookingForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-field',
        }),
        label='Укажите название мероприятия'
    )
    start_time = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'input-field',
        }),
        choices=TIMES_CHOICES,
        label='Выберите время начала'
    )
    end_time = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'input-field',
        }),
        choices=TIMES_CHOICES,
        label='Выберите время окончания'
    )
    date = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'input-field',
        }),
        choices=DATES_CHOICES,
        label='Выберите дату'
    )
    cabinet = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'input-field',
        }),
        queryset=Cabinet.objects.all(),
        empty_label='Выберите кабинет'
    )

    class Meta:
        model = Event
        fields = ('title', 'date', 'start_time', 'end_time', 'cabinet')
