from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Prefetch
from django.http import Http404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import permissions, serializers
from rest_framework.decorators import action

from booking.permissions import PermissionMixin, IsOwnerEvent
from booking.models import Cabinet, Event
from booking.serializers import CabinetListSerializer, CabinetDetailSerializer, EventSerializer
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
        event = self.get_object().event_cabinet.values('id', 'title', 'start_time', 'end_time', 'owner__username')
        return Response(create_schedule(list(event)), status=201)


class EventView(PermissionMixin, ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsOwnerEvent]
    permission_classes_by_action = {
        'list': [permissions.AllowAny],
        'retrieve': [permissions.AllowAny],
        'create': [permissions.IsAuthenticated],
    }

    def get_queryset(self):
        return Event.objects.select_related('owner') \
            .prefetch_related(Prefetch('visitors', queryset=User.objects.only('username'))) \
            .only('owner__username', 'title', 'cabinet__room_number', 'start_time', 'end_time') \
            .filter(cabinet__room_number=self.kwargs.get('room_number'))

    def perform_create(self, serializer):
        try:
            serializer.save(owner=self.request.user)
        except IntegrityError as exp:
            if 'check_datetime' in str(exp):
                error_message = 'Время окончания должно быть больше начала'
            else:
                error_message = f'Указанное время занято'
            raise serializers.ValidationError(error_message)
        except ValidationError as exp:
            raise serializers.ValidationError(exp.messages)
