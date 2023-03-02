from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import exceptions, generics, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import filters
from .models import User
from rest_framework.decorators import action

from .serializers import RegistrationSerializer, TokenSerializer, UserSerializer
from api.permissions import AdminPermission, AuthorStaffOrReadOnlyPermission


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

class UsersListCreateView(generics.ListCreateAPIView):
    http_method_names = ['get', 'post']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)
    permission_classes = (AdminPermission,)



class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ['get', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)
    pagination_class = (AuthorStaffOrReadOnlyPermission,)

    def get_object(self):
        username = self.kwargs.get('username')
        if username == 'me':
            return self.request.user
        try:
            user = get_object_or_404(User, username=username)
        except Http404:
            raise exceptions.ValidationError("Такого пользователя несуществует")
        return user