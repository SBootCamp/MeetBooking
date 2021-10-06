from django import forms

from booking.models import Event, Cabinet
from booking.services import create_date_choices, create_time_choices

BLANK_CHOICE = (('', '----'),)


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
        choices=BLANK_CHOICE + create_time_choices(),
        label='Выберите время начала'
    )
    end_time = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'input-field',
        }),
        choices=BLANK_CHOICE + create_time_choices(),
        label='Выберите время окончания'
    )
    date = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'input-field',
        }),
        choices=BLANK_CHOICE + create_date_choices(),
        label='Выберите дату'
    )
    cabinet = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'input-field',
        }),
        queryset=Cabinet.objects.all(),
        empty_label='----',
        label='Выберите кабинет'
    )

    class Meta:
        model = Event
        fields = ('title', 'date', 'start_time', 'end_time', 'cabinet')
