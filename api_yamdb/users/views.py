from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import exceptions, generics, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import filters
from .models import User
from rest_framework.decorators import action

from .serializers import RegistrationSerializer, TokenSerializer, UserSerializer
from api.permissions import AdminPermission, MePermission


class RegistrationViewSet(viewsets.ModelViewSet):
    """
    Разрешить всем пользователям (аутентифицированным и нет)
    доступ к данному эндпоинту.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


class TokenView(APIView):
    """
    Получить токен с помощью username и confirmation_code.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.initial_data.get('username')
            user = get_object_or_404(User, username=username)
            confirmation_code = serializer.initial_data.get(
                'confirmation_code'
            )

            if user.confirmation_code != confirmation_code:
                return Response(
                    {"confirmation_code": "incorrect"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            refresh = RefreshToken.for_user(user)
            return Response(
                {'token': str(refresh.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# class UserRetrieveUpdateAPIView(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = UserSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ('username',)

#     def get_object(self):
#         return self.request.user

#     @action(detail=True, methods=['get, patch'])
#     def me(self, request):
#         return self.retrieve(request, request.user)

# class UsersListCreateView(generics.ListCreateAPIView):
#     http_method_names = ['get', 'post']
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ('username',)
#     permission_classes = (AdminPermission,)
#     # Если значение поля role не передано в запросе,
#     # то устанавливаем значение поля role по умолчанию на user.
#     def perform_create(self, serializer):
#         serializer.save(role=self.request.data.get('role', 'user'))

# # Попробовать объеденить
# class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     http_method_names = ['get', 'patch', 'delete']
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ('username',)
#     ROLES = ['admin', 'user', 'moderator']

#     def get_object(self):
#         username = self.kwargs.get('username')
#         if username == 'me':
#             return self.request.user
#         try:
#             user = get_object_or_404(User, username=username)
#         except Http404:
#             raise exceptions.ValidationError("Такого пользователя несуществует")
#         return user


#     def partial_update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(
#             instance,
#             data=request.data,
#             partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         role = request.data.get('role')
#         if role and role not in self.ROLES:
#             return Response(
#                 {'role': 'Invalid role'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         self.perform_update(serializer)
#         return Response(serializer.data)
    
#     def destroy(self, request, *args, **kwargs):
#         if self.kwargs.get('username') == 'me':
#             return Response(
#                 {'Error': 'Нельзя удалить свой профиль'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED
#             )
#         return super().destroy(request, *args, **kwargs)
    
#     def get_permissions(self):
#         if self.kwargs.get('username') == 'me':
#             self.permission_classes = (MePermission,)
#         else:
#             self.permission_classes = (AdminPermission,)
#         return super(UserRetrieveUpdateDestroyView, self).get_permissions()
    

class UsersViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)
    ROLES = ['admin', 'user', 'moderator']

    def get_object(self):
        username = self.kwargs.get('pk')
        if username == 'me':
            return self.request.user
        try:
            user = get_object_or_404(User, username=username)
        except Http404:
            raise exceptions.ValidationError("Такого пользователя несуществует")
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
    
    def get_permissions(self):
        if self.kwargs.get('pk') == 'me':
            self.permission_classes = (MePermission,)
        elif self.kwargs.get('pk') is not None:
            self.permission_classes = (AdminPermission,)
        else:
            self.permission_classes = (AdminPermission,)
        return super(UsersViewSet, self).get_permissions()