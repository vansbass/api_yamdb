from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() #заменим позже на переопределенную модель


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'

class Title(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre,
        related_name='genre'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category'
    )
    year = models.IntegerField()

    def __str__(self):
        return f'{self.name}'

class Review(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    score = models.IntegerField()


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
