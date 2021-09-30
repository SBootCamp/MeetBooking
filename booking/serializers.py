from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Cabinet, Event


class CustomerHyperlink(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'pk': obj.room_number
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)


class CabinetListSerializer(serializers.ModelSerializer):
    url = CustomerHyperlink(view_name='cabinets-detail')

    class Meta:
        model = Cabinet
        fields = ('room_number', 'floor', 'place_count', 'tv', 'projector', 'url')


class CabinetDetailSerializer(CabinetListSerializer):
    url = CustomerHyperlink(view_name='cabinets-schedule')


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


# TODO: уточнить как будут записываться посетители
class EventSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(label='Дата и время начала')
    end_time = serializers.DateTimeField(label='Дата и время окончания')
    owner = serializers.SerializerMethodField()
    visitors = VisitorSerializer(many=True)

    def get_owner(self, obj):
        return obj.owner.username

    class Meta:
        model = Event
        fields = ('id', 'title', 'start_time', 'end_time', 'owner', 'cabinet', 'visitors')
