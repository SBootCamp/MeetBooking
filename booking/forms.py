from django import forms
from django.contrib.auth.models import User

from booking.models import Event
from booking.services import create_date_choices, create_time_choices

BLANK_CHOICE = (('', '----'),)


class EventForm(forms.ModelForm):
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
    visitors = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(attrs={
            'class': 'select-field',
        }),
        queryset=User.objects.only('username'),
        label='Кого пригласить',
        required=False,
    )

    class Meta:
        model = Event
        fields = ('title', 'start_time', 'end_time', 'visitors')

    def clean(self):
        data = self.cleaned_data
        date = data['date']
        data['start_time'] = f"{date}T{data['start_time']}Z"
        data['end_time'] = f"{date}T{data['end_time']}Z"
        return data
