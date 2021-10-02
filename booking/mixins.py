class PermissionMixin:
    """Mixin permissions for action"""
    permission_classes_by_action = None

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
