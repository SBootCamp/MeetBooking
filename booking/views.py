from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import Http404
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import permissions, serializers
from booking.models import Cabinet, Event
from booking.serializers import CabinetListSerializer, CabinetDetailSerializer, EventSerializer
from booking.services import create_schedule
from booking.utils.errors_draft import ResponseError
from booking.utils.processing_errors_sql import get_message_error
from booking.viewsets import RetrieveListCreateViewSet


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


class EventView(RetrieveListCreateViewSet):
    permission_classes = [permissions.AllowAny]
    permission_classes_by_action = {'create': [permissions.IsAuthenticated]}
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.select_related('cabinet', 'owner') \
            .filter(cabinet__room_number=self.kwargs.get('room_number'))

    def perform_create(self, serializer):
        try:
            serializer.save(owner=self.request.user)
        except IntegrityError as exp:
            error_message = get_message_error(exp)
            raise serializers.ValidationError(error_message)
