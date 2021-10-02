from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Cabinet, Event


class CustomerHyperlinkCabinet(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'pk': obj.room_number,
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)


class CustomerHyperlinkEvent(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'room_number': obj.cabinet.room_number,
            'pk': obj.id
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)


class CabinetListSerializer(serializers.ModelSerializer):
    url = CustomerHyperlinkCabinet(view_name='cabinets-detail')

    class Meta:
        model = Cabinet
        fields = ('room_number', 'floor', 'place_count', 'tv', 'projector', 'url')


class CabinetDetailSerializer(serializers.ModelSerializer):
    schedule = CustomerHyperlinkCabinet(view_name='cabinets-schedule')

    class Meta:
        model = Cabinet
        fields = ('room_number', 'floor', 'place_count', 'tv', 'projector', 'schedule')


class EventListSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(label='Дата и время начала')
    end_time = serializers.DateTimeField(label='Дата и время окончания')
    owner = serializers.StringRelatedField(read_only=True)
    url = CustomerHyperlinkEvent(view_name='events-detail')
    cabinet = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'start_time', 'end_time', 'owner', 'cabinet', 'url')


class EventDetailSerializer(EventListSerializer):
    visitors = serializers.StringRelatedField(many=True, read_only=True)
    cabinet = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'start_time', 'end_time', 'owner', 'cabinet', 'visitors')


class EventCreateUpdateSerializer(EventDetailSerializer):
    visitors = serializers.PrimaryKeyRelatedField(queryset=User.objects.only('username'), many=True)
    cabinet = serializers.PrimaryKeyRelatedField(queryset=Cabinet.objects.only('room_number'))
