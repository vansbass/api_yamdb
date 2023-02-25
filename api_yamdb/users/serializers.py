from rest_framework import serializers
from django.core.mail import send_mail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'The word "me" is prohibited for registration'
            )
        return username

    def create(self, validated_data):
        confirmation_code = User.objects.make_random_password(length=10)
        user = User.objects.create(
            confirmation_code=confirmation_code,
            **validated_data)
        user.save()
        send_mail('Confirmation code for the Yambd Api',
                  f'{confirmation_code}',
                  user.email, ['noreply@yambd.ru'],
                  fail_silently=False,
                  )
        return user


class TokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(
        max_length=10,
    )
    username = serializers.CharField(max_length=150)