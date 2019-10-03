from django.contrib import admin

from . import models
# Register your models here.
#admin.site.register(models.Book)
admin.site.register(models.Genre)

@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'author', 'display_genre')
    list_filter = ('genre', 'author')
