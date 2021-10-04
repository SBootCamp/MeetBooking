from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.http import Http404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action

from booking.mixins import PermissionMixin, SerializerMixin
from booking.permissions import IsOwnerEvent, BookingTimeNotPassed
from booking.models import Cabinet, Event
from booking.serializers import CabinetListSerializer, CabinetDetailSerializer, EventListSerializer, \
    EventDetailSerializer, EventCreateUpdateSerializer
from booking.services import create_schedule


class CabinetViewSet(SerializerMixin, ReadOnlyModelViewSet):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetListSerializer
    serializer_class_by_action = {'retrieve': CabinetDetailSerializer}

    def get_object(self):
        try:
            return Cabinet.objects.get(room_number=self.kwargs.get('pk'))
        except Cabinet.DoesNotExist:
            raise Http404

    @action(detail=True, methods=['get'])
    def schedule(self, *args, **kwargs):
        event = Event.room_objects.filter(cabinet__room_number=self.kwargs.get('pk')).values()
        return Response(create_schedule(event), status=200)


class EventViewSet(PermissionMixin, SerializerMixin, ModelViewSet):
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
        queryset = Event.room_objects.filter(cabinet__room_number=self.kwargs.get('room_number'))
        if self.action == 'list':
            return queryset
        return queryset.prefetch_related(Prefetch('visitors', queryset=User.objects.only('username')))


