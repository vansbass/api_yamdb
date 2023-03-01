from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters, status, mixins, generics
from rest_framework.viewsets import ModelViewSet

from .permissions import (
    AdminPermission, AdminOrReadOnlyPermission,
    AuthorStaffOrReadOnlyPermission
)
from reviews.models import (
    Category, Genre, Review, Title
)
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleSerializerRead, TitleSerializerWrite
)
from rest_framework.decorators import action


class CategoriesView(generics.ListCreateAPIView):
    http_method_names = ['get', 'post', 'delete']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnlyPermission,)
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
    permission_classes = (AdminOrReadOnlyPermission,)
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
    permission_classes = (AuthorStaffOrReadOnlyPermission,)

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
    permission_classes = (AuthorStaffOrReadOnlyPermission,)

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
    permission_classes = (AdminOrReadOnlyPermission,)
 
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerRead
        return TitleSerializerWrite
    
    def perform_create(self, serializer):
        genre_slugs = self.request.data.get('genre')
        genres = Genre.objects.filter(slug__in=genre_slugs)
        serializer.save(genre=genres)
 
    # def perform_create(self, serializer):
    #     category_slug = self.request.data['category']
    #     genre = self.request.data['genre']
    #     category = get_object_or_404(Category, slug=category_slug)
    #     genres = []
    #     for item in genre:
    #         genres.append(get_object_or_404(Genre, slug=item))
    #     serializer.save(category=category, genre=genres)