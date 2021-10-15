from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from booking.models import Cabinet, Event
from booking.services import create_datetime_list


class CustomerHyperlinkCabinet(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'pk': obj.name,
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)


class CustomerHyperlinkEvent(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'name': obj.cabinet.name,
            'pk': obj.id
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)


class CabinetListSerializer(serializers.ModelSerializer):
    url = CustomerHyperlinkCabinet(view_name='cabinets-detail')

    class Meta:
        model = Cabinet
        fields = ('room_number', 'name', 'floor', 'place_count', 'tv', 'projector', 'url')


class CabinetDetailSerializer(serializers.ModelSerializer):
    schedule = CustomerHyperlinkCabinet(view_name='cabinets-schedule')

    class Meta:
        model = Cabinet
        fields = ('room_number', 'name', 'floor', 'place_count', 'tv', 'projector', 'schedule')


class EventListSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(label='Дата и время начала')
    end_time = serializers.DateTimeField(label='Дата и время окончания')
    owner = serializers.StringRelatedField(read_only=True)
    cabinet = serializers.StringRelatedField(read_only=True)
    url = CustomerHyperlinkEvent(view_name='events-detail')

    class Meta:
        model = Event
        fields = ('id', 'title', 'start_time', 'end_time', 'owner', 'cabinet', 'url')


class EventDetailSerializer(EventListSerializer):
    visitors = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'start_time', 'end_time', 'owner', 'cabinet', 'visitors')


class EventCreateUpdateSerializer(EventDetailSerializer):
    visitors = serializers.PrimaryKeyRelatedField(queryset=User.objects.only('username'), many=True)
    cabinet = serializers.PrimaryKeyRelatedField(queryset=Cabinet.objects.only('name'))
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_start_time(self, value):
        if value not in create_datetime_list():
            raise serializers.ValidationError('Некорректная дата или время начала мероприятия')
        return value

    def validate_end_time(self, value):
        if value not in create_datetime_list():
            raise serializers.ValidationError('Некорректная дата или время окончания мероприятия')
        return value

    def save(self, **kwargs):
        try:
            return super().save(**kwargs)
        except IntegrityError as exp:
            if 'check_datetime' in str(exp):
                error_message = 'Время окончания мероприятия должно быть больше начала'
            else:
                error_message = 'Указанное время занято'
            raise serializers.ValidationError(error_message)
        except ValidationError as exp:
            raise serializers.ValidationError(exp.messages)
