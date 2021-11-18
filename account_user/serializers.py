from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from meet_booking.settings import LOWER_VALUE_LENGTH_NAME, \
    UPPER_VALUE_LENGTH_NAME, TOKEN_MAX_LENGTH


class RegistrationUserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True, label="Повторите пароль",
                                      validators=[validate_password])
    email = serializers.EmailField(allow_blank=True, allow_null=True)
    token = serializers.CharField(max_length=TOKEN_MAX_LENGTH, read_only=True,
                                  allow_blank=True, allow_null=True)

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
            raise serializers.ValidationError("Пароли не совпадают")

        return data

    def validate_username(self, username):
        if len(username) < LOWER_VALUE_LENGTH_NAME or len(username) > UPPER_VALUE_LENGTH_NAME:
            raise serializers.ValidationError(f"Имя пользователя должно содержать от "
                                              f"{LOWER_VALUE_LENGTH_NAME} "f"до "
                                              f"{UPPER_VALUE_LENGTH_NAME} символов.")
        return username

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        return user
