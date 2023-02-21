from django.contrib import admin

from .models import Category, Genre, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'genre',
        'category',
        'year'
    )
    list_editable = ('genre', 'category')

admin.site.register(Title, TitleAdmin)
admin.site.register(Genre)
admin.site.register(Category)
