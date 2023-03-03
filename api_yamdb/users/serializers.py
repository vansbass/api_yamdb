from django.core.mail import send_mail
from rest_framework import serializers

from users.models import User


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


class UserSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов User. """
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']
