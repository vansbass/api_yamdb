from django.contrib import admin
from users.models import User

from .models import Category, Genre, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'year'
    )
    list_editable = ('category',)

admin.site.register(User)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre)
admin.site.register(Category)
