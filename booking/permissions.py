from rest_framework.permissions import BasePermission


class PermissionMixin:
    """Миксин permissions для action"""
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class IsOwnerEvent(BasePermission):
    """Организатор мероприятия"""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
