from datetime import datetime

from rest_framework import serializers
from django.db.models import Avg

from reviews.models import (
    Category, Comment, Genre, Review, Title
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        """Check that score in range 0 - 10"""
        if value > 10 or value < 0:
            raise serializers.ValidationError("Score not in range 0-10")
        return value

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        many=True, queryset=Genre.objects.all(), slug_field='slug'
    )
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        return rating

    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'rating', 'description', 'genre', 'category']
        read_only_fields = ['id']
    
    def validate_year(self, value):
        year_now = datetime.now().year
        if value > year_now:
            raise serializers.ValidationError("Будущиее еще не наступило")
        return value

    def create(self, validated_data):
        genre_data = validated_data.pop('genre', [])
        category_data = validated_data.pop('category', None)
        if category_data is not None:
            category = Category.objects.get(slug=category_data)
            validated_data['category'] = category
        instance = super().create(validated_data)
        for slug in genre_data:
            genre = Genre.objects.get(slug=slug)
            instance.genre.add(genre)
        instance.save()
        return instance

    def to_representation(self, instance):
        self.fields['category'] = CategorySerializer()
        return super().to_representation(instance)
