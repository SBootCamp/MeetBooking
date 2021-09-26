from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class PermissionMixin:
    """Миксин permissions для action"""
    permission_classes_by_action = None

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class RetrieveListCreateViewSet(mixins.RetrieveModelMixin,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                PermissionMixin,
                                GenericViewSet):
    pass
