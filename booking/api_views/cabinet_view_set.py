from django.http import Http404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from booking.mixins import SerializerMixin
from booking.models import Cabinet, Event
from booking.serializers import CabinetListSerializer, CabinetDetailSerializer
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