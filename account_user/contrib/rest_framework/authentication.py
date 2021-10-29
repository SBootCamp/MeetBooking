import datetime
from datetime import timezone

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication as DrfTokenAutentification
from rest_framework import exceptions
from django.contrib.auth.models import User


class TokenAuthentication(DrfTokenAutentification):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
            diff_dates = datetime.datetime.now(timezone.utc) - token.created

            if diff_dates.days > 30:
                user = User.objects.get(id=token.user_id)
                token.delete()
                token = model.objects.create(user=user)

        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(('User inactive or deleted.'))

        return (token.user, token)
