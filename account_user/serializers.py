from rest_framework import serializers
from django.contrib.auth.models import User


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
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
