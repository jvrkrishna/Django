from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at')
    list_display_links = ('title',)
    list_filter = ('created_at', 'author')

admin.site.register(Post, PostAdmin)
