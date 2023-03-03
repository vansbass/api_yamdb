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


class CategoriesOrGenresViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)

    def get_queryset(self):
        if self.basename == 'categories':
            return Category.objects.all()
        elif self.basename == 'genres':
            return Genre.objects.all()
        return None

    def get_serializer_class(self):
        if self.basename == 'categories':
            self.serializer_class = CategorySerializer
        elif self.basename == 'genres':
            self.serializer_class = GenreSerializer
        return super(CategoriesOrGenresViewSet, self).get_serializer_class()

    def get_object(self):
        slug = self.kwargs.get('pk')
        obj = None
        try:
            if self.basename == 'categories':
                obj = get_object_or_404(Category, slug=slug)
            elif self.basename == 'genres':
                obj = get_object_or_404(Genre, slug=slug)
        except Http404:
            raise exceptions.ValidationError('Такого объекта нет')
        return obj

    def retrieve(self, request, *args, **kwargs):
        if self.kwargs.get('pk') is not None and self.request.method == 'GET':
            return Response(
                {'Warning': 'Method not Allowed'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().retrieve(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE']:
            self.permission_classes = (AdminPermission,)
        if self.kwargs.get('pk') is not None:
            self.permission_classes = (AdminPermission,)
        return super(CategoriesOrGenresViewSet, self).get_permissions()


class ReviewOrCommentViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (AuthorStaffOrReadOnlyPermission,)

    def get_queryset(self):
        obj = None
        try:
            if self.basename == 'reviews':
                obj = get_object_or_404(
                    Title, pk=self.kwargs.get('title_id')
                )
            elif self.basename == 'comments':
                obj = get_object_or_404(
                    Review, pk=self.kwargs.get('review_id')
                )
        except Http404:
            raise exceptions.ValidationError('Такого объекта нет')
        if self.basename == 'reviews':
            return obj.reviews.all()
        elif self.basename == 'comments':
            return obj.comments.all()
        return obj

    def get_serializer_class(self):
        if self.basename == 'reviews':
            self.serializer_class = ReviewSerializer
        elif self.basename == 'comments':
            self.serializer_class = CommentSerializer
        return super(ReviewOrCommentViewSet, self).get_serializer_class()

    def perform_create(self, serializer):
        if self.basename == 'reviews':
            serializer.save(
                author=self.request.user,
                title=get_object_or_404(
                    Title, pk=self.kwargs.get('title_id')
                )
            )
        elif self.basename == 'comments':
            serializer.save(
                author=self.request.user,
                review=get_object_or_404(
                    Review, pk=self.kwargs.get('review_id')
                )
            )


class TitleViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnlyPermission,)
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
