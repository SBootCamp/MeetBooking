from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Prefetch
from django.http import Http404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import permissions, serializers
from rest_framework.decorators import action

from booking.mixins import PermissionMixin
from booking.permissions import IsOwnerEvent, BookingTimeNotPassed
from booking.models import Cabinet, Event
from booking.serializers import CabinetListSerializer, CabinetDetailSerializer, EventListSerializer, \
    EventDetailSerializer, EventCreateUpdateSerializer
from booking.services import create_schedule


class CabinetView(ReadOnlyModelViewSet):
    queryset = Cabinet.objects.all()

    def get_object(self):
        try:
            return Cabinet.objects.get(room_number=self.kwargs.get('pk'))
        except Cabinet.DoesNotExist:
            raise Http404

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CabinetDetailSerializer
        return CabinetListSerializer

    @action(detail=True, methods=['get'])
    def schedule(self, *args, **kwargs):
        event = self.get_object().event_cabinet \
            .filter(start_time__month=timezone.now().month).values(
            'id', 'title', 'start_time',
            'end_time', 'owner__username'
        )
        return Response(create_schedule(event), status=201)


class EventView(PermissionMixin, ModelViewSet):
    permission_classes = [IsOwnerEvent, BookingTimeNotPassed]
    permission_classes_by_action = {
        'list': [permissions.AllowAny],
        'retrieve': [permissions.AllowAny],
        'create': [permissions.IsAuthenticated],
    }

    def get_queryset(self):
        queryset = Event.objects.select_related('cabinet', 'owner') \
            .only('owner__username', 'title', 'cabinet__room_number', 'start_time', 'end_time') \
            .filter(
            cabinet__room_number=self.kwargs.get('room_number'),
            start_time__month=timezone.now().month
        )
        if self.action != 'list':
            return queryset.prefetch_related(Prefetch('visitors', queryset=User.objects.only('username')))
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventDetailSerializer
        elif self.action == 'list':
            return EventListSerializer
        return EventCreateUpdateSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(owner=self.request.user)
        except IntegrityError as exp:
            if 'check_datetime' in str(exp):
                error_message = 'Время окончания мероприятия должно быть больше начала'
            else:
                error_message = 'Указанное время занято'
            raise serializers.ValidationError(error_message)
        except ValidationError as exp:
            raise serializers.ValidationError(exp.messages)
