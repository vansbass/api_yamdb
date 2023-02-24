from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):

    username = models.CharField(unique=True, blank=False, max_length=150)
    email = models.EmailField(unique=True, blank=False, max_length=254)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bio = models.TextField(max_length=500, blank=True)
    role = models.ChoiceField(choices=ROLE_CHOICES, default='user', max_length=9)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'
