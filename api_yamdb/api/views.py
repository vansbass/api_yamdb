from rest_framework.viewsets import ModelViewSet

from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleSerializer
)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer


class GenreViewSet(ModelViewSet):
    serializer_class = GenreSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer


class TitleViewSet(ModelViewSet):
    serializer_class = TitleSerializer