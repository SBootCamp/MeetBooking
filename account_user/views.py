from http import HTTPStatus

from rest_framework import generics
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers

from .contrib.rest_framework.authentication import TokenAuthentication
from .serializers import RegistrationUserSerializer
from booking.models import Event


class RegistrationView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistrationUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'status_code': HTTPStatus.CREATED,
            'message': "Пользователь успешно создан",
        })


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key
        })


class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = serializers.serialize("json", Event.objects.filter(visitors=str(request.user.id)))
        content = {
            'events': data,
            'username': str(request.user.username),
            'email': str(request.user.email)
        }

        return Response(content)
