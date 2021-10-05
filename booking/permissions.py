from django.utils import timezone
from rest_framework.permissions import BasePermission


class IsOwnerEvent(BasePermission):
    """Организатор мероприятия"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class BookingTimeNotPassed(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.end_time > timezone.now()
