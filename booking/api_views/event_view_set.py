from django.contrib.auth.models import User
from django.db.models import Prefetch
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from booking.mixins import PermissionMixin, SerializerMixin
from booking.permissions import IsOwnerEvent, BookingTimeNotPassed
from booking.models import Event
from booking.serializers import EventListSerializer, \
    EventDetailSerializer, EventCreateUpdateSerializer


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