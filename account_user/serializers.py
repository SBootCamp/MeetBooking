import logging

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


logger = logging.getLogger(__name__)


class RegistrationUserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True, label="Повторите пароль",
                                      validators=[validate_password])
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
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Пароли не совпадают')

        return data

    def validate_username(self, username):
        if len(username) < 6 or len(username) > 25:
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
