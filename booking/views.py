from django.core.exceptions import ValidationError
from django.http import Http404
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import permissions, serializers
from booking.models import Cabinet, Event
from booking.serializers import CabinetSerializer, EventSerializer
from booking.viewsets import RetrieveListCreateViewSet


class CabinetView(ReadOnlyModelViewSet):
    serializer_class = CabinetSerializer
    queryset = Cabinet.objects.all()

    def get_object(self):
        try:
            return Cabinet.objects.get(room_number=self.kwargs.get('pk'))
        except Cabinet.DoesNotExist:
            raise Http404


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
        except ValidationError as e:
            raise serializers.ValidationError(' '.join(e.message_dict.get('__all__')))
