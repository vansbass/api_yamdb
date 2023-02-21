from rest_framework import serializers

from reviews.models import (
    Category, Comment, Genre, Review, Title
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='', #Его пока нет
        read_only=True
    )
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='',  #Его пока нет
        read_only=True
    )
    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date']


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=True,
        many=True,
    )
    class Meta:
        model = Title
        fields = ['name', 'year', 'description', 'genre', 'category']