from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters, status, mixins, generics
from rest_framework.viewsets import ModelViewSet

from .permissions import AuthorAdminOrReadOnlyPermission, AdminPermission
from reviews.models import (
    Category, Genre, Review, Title
)
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleSerializer
)
from rest_framework.decorators import action


class CategoriesView(generics.ListCreateAPIView):
    http_method_names = ['get', 'post', 'delete']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminPermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class CategoryDeleteView(generics.DestroyAPIView):
    http_method_names = ['get', 'post', 'delete']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminPermission,)

    def get_object(self):
        print(self.kwargs)
        slug = self.kwargs.get('slug')
        print(slug)
        return get_object_or_404(Category, slug=slug)


class GenreView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminPermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class GenreDeleteView(generics.DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminPermission,)

    def get_object(self):
        print(self.kwargs)
        slug = self.kwargs.get('slug')
        print(slug)
        return get_object_or_404(Genre, slug=slug)


class CommentViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminOrReadOnlyPermission,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        )


class ReviewViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminOrReadOnlyPermission,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        )


class TitleViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Title.objects.all()
    permission_classes = [AdminPermission, ]
    serializer_class = TitleSerializer
