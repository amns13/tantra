from django.contrib import admin
from .models import Post, PostComment


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
    )


class PostCommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'author'
    )


admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, PostCommentAdmin)
