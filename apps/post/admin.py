# -*- coding: utf-8 -*-
from django.contrib import admin

from core.admin import CustomModelAdmin
from .models import Post, PostComment, PostLike, PostCommentLike


@admin.register(Post)
class PostAdmin(CustomModelAdmin):
    list_display = (
        'pkid',
        'uuid',
        'title',
        'author',
        'status',
        'created_at',
        'updated_at',
        'is_active',
        'created_by',
        'updated_by',
    )
    list_filter = (
        'is_active',
        'status',
        'author',
    )
    date_hierarchy = 'created_at'


@admin.register(PostComment)
class PostCommentAdmin(CustomModelAdmin):
    list_display = (
        'pkid',
        'uuid',
        'author',
        'post',
        'body',
        'created_at',
        'updated_at',
        'is_active',
        'created_by',
        'updated_by',
    )
    list_filter = (
        'is_active',
        'author',
        'post',
    )
    date_hierarchy = 'created_at'


@admin.register(PostLike)
class PostLikeAdmin(CustomModelAdmin):
    list_display = (
        'pkid',
        'uuid',
        'user',
        'post',
        'created_at',
        'updated_at',
        'is_active',
        'created_by',
        'updated_by',
    )
    list_filter = (
        'is_active',
        'user',
        'post',
    )
    date_hierarchy = 'created_at'


@admin.register(PostCommentLike)
class PostCommentLikeAdmin(CustomModelAdmin):
    list_display = (
        'pkid',
        'uuid',
        'created_at',
        'updated_at',
        'user',
        'comment',
        'is_active',
        'created_by',
        'updated_by',
    )
    list_filter = (
        'is_active',
        'user',
        'comment',
    )
    date_hierarchy = 'created_at'
