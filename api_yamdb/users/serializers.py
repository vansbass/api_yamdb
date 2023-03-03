from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z$',
        required=True,
        max_length=150
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'The word "me" is prohibited for registration'
            )
        return username


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(
        max_length=10, required=True
    )
    username = serializers.CharField(
        max_length=150, required=True
    )

    def validate(self, data):
        user = get_object_or_404(
            User,
            username=data['username']
        )
        if user.confirmation_code != data['confirmation_code']:
            raise serializers.ValidationError(
                'Не совпадает код подтверждения!'
            )
        return data

    class Meta:
        fields = ('username', 'confirmation_code',)
        model = User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        ]
