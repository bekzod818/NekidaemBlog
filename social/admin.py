from django.contrib import admin
from .models import Blog, Post


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'user')
    list_display_links = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post)
