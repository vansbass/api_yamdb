from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, filters, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.filters import TitleFilter
from api.permissions import (
    AdminOrReadOnlyPermission, AdminPermission,
    AuthorStaffOrReadOnlyPermission
)
from api.serializers import (
    CategorySerializer, CommentSerializer,
    GenreSerializer, ReviewSerializer,
    TitleSerializer
)
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)

    def get_object(self):
        slug = self.kwargs.get('pk')
        try:
            return get_object_or_404(Category, slug=slug)
        except Http404:
            raise exceptions.ValidationError('Такой категории нет')

    def retrieve(self, request, *args, **kwargs):
        if (
            self.kwargs.get('pk') is not None
            and self.request.method == 'GET'
        ):
            return Response(
                {'Warning': 'Method not Allowed'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().retrieve(request, *args, **kwargs)

    def get_permissions(self):
        if (
            self.request.method in ['POST', 'DELETE']
            or self.kwargs.get('pk') is not None
        ):
            self.permission_classes = (AdminPermission,)
        return super(CategoryViewSet, self).get_permissions()


class GenresViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)

    def get_object(self):
        slug = self.kwargs.get('pk')
        try:
            return get_object_or_404(Genre, slug=slug)
        except Http404:
            raise exceptions.ValidationError('Такого жанра нет')

    def retrieve(self, request, *args, **kwargs):
        if (
            self.kwargs.get('pk') is not None
            and self.request.method == 'GET'
        ):
            return Response(
                {'erorr': 'Method not Allowed'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().retrieve(request, *args, **kwargs)

    def get_permissions(self):
        if (
            self.request.method in ['POST', 'DELETE']
            or self.kwargs.get('pk') is not None
        ):
            self.permission_classes = (AdminPermission,)
        return super(GenresViewSet, self).get_permissions()


class CommentViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = CommentSerializer
    permission_classes = (AuthorStaffOrReadOnlyPermission,)

    def get_queryset(self):
        try:
            review = get_object_or_404(
                Review, pk=self.kwargs.get('review_id')
            )
        except Http404:
            raise exceptions.ValidationError('Такого ревью нет')
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        )


class ReviewViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ReviewSerializer
    permission_classes = (AuthorStaffOrReadOnlyPermission,)

    def get_queryset(self):
        try:
            title = get_object_or_404(
                Title, pk=self.kwargs.get('title_id')
            )
        except Http404:
            raise exceptions.ValidationError('Такого произведения нет')
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        )


class TitleViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnlyPermission,)
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
