class PermissionMixin:
    """Mixin permissions for action"""
    permission_classes_by_action = None

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class GetSerializerClassMixin:
    """Mixin serializers for action"""
    serializer_class_by_action = None

    def get_serializer_class(self):
        try:
            return self.serializer_class_by_action[self.action]
        except KeyError:
            return super().get_serializer_class()
