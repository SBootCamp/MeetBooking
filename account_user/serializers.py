import logging

from rest_framework import serializers
from django.contrib.auth.models import User
from django.core import exceptions
import django.contrib.auth.password_validation as validators


logger = logging.getLogger(__name__)


class RegistrationUserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True, label="Повторите пароль")
    email = serializers.EmailField(allow_blank=True, allow_null=True)
    token = serializers.CharField(max_length=255, read_only=True, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            'token',
            "password2",
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data['password']

        try:
            validators.validate_password(password=password)
        except exceptions.ValidationError as e:
            errors = list(e.messages)
            for err in errors:
                logger.debug(err)

            raise serializers.ValidationError(list(e.messages))

        if data['password'] != data['password2']:
            logger.debug("Пароли не совпадают")
            raise serializers.ValidationError('Пароли не совпадают')

        return data

    def validate_username(self, username):
        if len(username) < 6 or len(username) > 25:
            logger.debug("Имя пользователя должно содержать от 6 до 15 символов.")
            raise serializers.ValidationError('Имя пользователя должно содержать от 6 до 15 символов.')

        return username

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
