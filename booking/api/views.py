from datetime import timedelta
from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.db.models import Prefetch
from rest_framework import permissions, serializers
from django.conf import settings

from booking.api.mixins import PermissionMixin
from booking.api.permissions import IsOwnerEvent, BookingTimeNotPassed
from booking.api.serializers import EventListSerializer, \
    EventDetailSerializer, EventCreateUpdateSerializer
from booking.api.mixins import GetSerializerClassMixin
from booking.models import Cabinet, Event
from booking.api.serializers import CabinetListSerializer, CabinetDetailSerializer
from booking.services import create_schedule, create_datetime_list


class CabinetViewSet(GetSerializerClassMixin, ReadOnlyModelViewSet):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetListSerializer
    serializer_class_by_action = {'retrieve': CabinetDetailSerializer}

    def get_object(self):
        return get_object_or_404(Cabinet, name=self.kwargs.get('pk'))

    @action(detail=True, methods=['get'])
    def schedule(self, *args, **kwargs):
        event = Event.room_objects.filter(cabinet__name=self.kwargs.get('pk')).values()
        return Response(create_schedule(event), status=200)


class EventViewSet(PermissionMixin, GetSerializerClassMixin, ModelViewSet):
    permission_classes = [IsOwnerEvent, BookingTimeNotPassed]
    serializer_class = EventCreateUpdateSerializer
    permission_classes_by_action = {
        'list': [permissions.AllowAny],
        'retrieve': [permissions.AllowAny],
        'create': [permissions.IsAuthenticated],
    }
    serializer_class_by_action = {
        'list': EventListSerializer,
        'retrieve': EventDetailSerializer,
    }

    def get_queryset(self):
        queryset = Event.room_objects.filter(cabinet__name=self.kwargs.get('name'))
        if self.action == 'list':
            return queryset
        return queryset.prefetch_related(Prefetch('visitors', queryset=User.objects.only('username')))

    def perform_create(self, serializer):
        data = serializer.validated_data
        duplication = data.pop('duplication')
        period_duplication = timedelta(days=settings.PERIOD_DUPLICATION_DAYS)
        try:
            with transaction.atomic():
                serializer.save()
                if duplication:
                    visitors = data.pop('visitors')
                    while data['start_time'] + period_duplication in create_datetime_list():
                        data['start_time'] += period_duplication
                        data['end_time'] += period_duplication
                        event = Event.objects.create(**data)
                        event.visitors.add(*visitors)
        except IntegrityError:
            raise serializers.ValidationError('Невозможно продублировать мероприятие')
