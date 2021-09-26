from calendar import monthrange

from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Cabinet, Event

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


class CustomerHyperlink(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'pk': obj.room_number
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)


class CabinetSerializer(serializers.ModelSerializer):
    url = CustomerHyperlink(view_name='cabinets-detail')

    class Meta:
        model = Cabinet
        fields = ('room_number', 'floor', 'place_count', 'tv', 'projector', 'url')


class EventSerializer(serializers.ModelSerializer):
    start_time = serializers.ChoiceField(choices=TIMES_CHOICES, label='Время начала')
    end_time = serializers.ChoiceField(choices=TIMES_CHOICES, label='Время окончания')
    date = serializers.ChoiceField(choices=DATES_CHOICES, label='Дата проведения')
    owner = serializers.SlugField(source='owner.username', read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'date', 'start_time', 'end_time', 'cabinet', 'owner')

