from datetime import datetime
import re

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators
from django.db.models import Avg

from reviews.models import (
    Category, Comment, Genre, Review, Title
)
from users.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')

    def validate_slug(self, value):
        if not re.match('^[-a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError('Некоректный slug')
        return value
    


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

    def validate_slug(self, value):
        if not re.match('^[-a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError('Некоректный slug')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        # Берем автора и тайтл из контекста
        author = self.context['request'].user
        title = get_object_or_404(
            Title,
            id=self.context['view'].kwargs['title_id']
        )
        # Если уже есть ревью на этот тайтл от автора, то рейзим ошибку
        if title.reviews.filter(author=author).exists():
            # Но разрешаем модератору делать PATCH и PUT-запрос
            if self.context['request'].method != ('PATCH' or 'PUT'):
                raise serializers.ValidationError('Вы можете оставить только один отзыв')
        return data

    def validate_score(self, value):
        """Check that score in range 0 - 10"""
        if value > 10 or value < 0:
            raise serializers.ValidationError("Score not in range 0-10")
        return value

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']
        

class TitleSerializerRead(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)
 
    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'rating', 'description', 'genre',
                  'category']
        
    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        if rating is not None:
            return round(rating)
        return None
    
    # def to_representation(self, instance):
    #     self.fields['genre'] = GenreSerializer(many=True)
    #     self.fields['category'] = CategorySerializer()
    #     return super().to_representation(instance)
    
    # def to_representation(self, instance):
    #     request = self.context.get('request')
    #     context = {'request': request}
    #     return TitleSerializerRead(instance, context=context).data
    
 
 
class TitleSerializerWrite(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
        )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all())
    rating = serializers.SerializerMethodField(read_only=True)
 
    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'rating', 'description', 'genre',
                  'category']
        read_only_fields = ['id']
        validators = [
            validators.UniqueTogetherValidator(
            queryset=Title.objects.all(),
            fields=['name', 'category'],
            message='Такая запись уже есть'
            )
        ]
        
    def validate_year(self, value):
        year_now = datetime.now().year
        if value > year_now:
            raise serializers.ValidationError(
                "Будущее еще не наступило")
        return value
 
    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        if rating is not None:
            return round(rating)
        return None
    
    def to_representation(self, instance):
        self.fields['genre'] = GenreSerializer(many=True)
        self.fields['category'] = CategorySerializer()
        return super().to_representation(instance)

    # def to_representation(self, instance):
    #     request = self.context.get('request')
    #     context = {'request': request}
    #     return TitleSerializerRead(instance, context=context).data
