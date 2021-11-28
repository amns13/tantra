# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Post, PostComment, PostLike, PostCommentLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated_at',
        'is_active',
        'title',
        'body',
        'author',
    )
    list_filter = ('created_at', 'updated_at', 'is_active', 'author')
    date_hierarchy = 'created_at'


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated_at',
        'is_active',
        'author',
        'body',
        'post',
    )
    list_filter = ('created_at', 'updated_at', 'is_active', 'author', 'post')
    date_hierarchy = 'created_at'


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'updated_at',
        'is_active',
        'id',
        'user',
        'post',
    )
    list_filter = ('created_at', 'updated_at', 'is_active', 'user', 'post')
    date_hierarchy = 'created_at'


@admin.register(PostCommentLike)
class PostCommentLikeAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'updated_at',
        'is_active',
        'id',
        'user',
        'comment',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'is_active',
        'user',
        'comment',
    )
    date_hierarchy = 'created_at'
