from api.permissions import AdminPermission, MePermission
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from users.serializers import SignupSerializer, TokenSerializer, UserSerializer


class AuthSignupAPIView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, created = User.objects.get_or_create(
                email=serializer.validated_data.get('email'),
                username=serializer.validated_data.get('username'),
            )
        except IntegrityError as error:
            return Response(f'{error}', status=status.HTTP_400_BAD_REQUEST)

        send_mail(
            'Код подтверждения',
            f'{user.confirmation_code}',
            'noreply@yambd.ru', [user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAPIView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username')
        )
        token = AccessToken.for_user(user)
        return Response(
            data={'token': str(token)},
            status=status.HTTP_200_OK
        )


class UsersViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)
    ROLES = ['admin', 'user', 'moderator']

    def get_permissions(self):
        if self.kwargs.get('pk') == 'me':
            self.permission_classes = (MePermission,)
        elif self.kwargs.get('pk') is not None:
            self.permission_classes = (AdminPermission,)
        else:
            self.permission_classes = (AdminPermission,)
        return super(UsersViewSet, self).get_permissions()

    def get_object(self):
        username = self.kwargs.get('pk')
        user = None
        if username == 'me':
            return self.request.user
        try:
            user = get_object_or_404(User, username=username)
        except Http404:
            raise exceptions.ValidationError(
                "Такого пользователя несуществует"
            )
        return user

    def perform_create(self, serializer):
        serializer.save(role=self.request.data.get('role', 'user'))

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        role = request.data.get('role')
        if role and role not in self.ROLES:
            return Response(
                {'role': 'Invalid role'},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if self.kwargs.get('pk') == 'me':
            return Response(
                {'Error': 'Нельзя удалить свой профиль'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)
