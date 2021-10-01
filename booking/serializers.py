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


class CabinetDetailSerializer(CabinetListSerializer):
    url = CustomerHyperlinkCabinet(view_name='cabinets-schedule')


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


# TODO: уточнить как будут записываться посетители
class EventListSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(label='Дата и время начала')
    end_time = serializers.DateTimeField(label='Дата и время окончания')
    owner = serializers.SerializerMethodField()
    url = CustomerHyperlinkEvent(view_name='event-detail')

    @staticmethod
    def get_owner(obj):
        return obj.owner.username

    class Meta:
        model = Event
        fields = ('id', 'title', 'start_time', 'end_time', 'owner', 'cabinet', 'url')


class EventCreateUpdateSerializer(EventListSerializer):

    class Meta:
        model = Event
        fields = ('id', 'title', 'start_time', 'end_time', 'owner', 'cabinet', 'visitors')

class EventDetailSerializer(EventCreateUpdateSerializer):
    visitors = VisitorSerializer(many=True, read_only=False)


