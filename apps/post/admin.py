# -*- coding: utf-8 -*-
from core.admin import CustomModelAdmin
from django.contrib import admin

from .models import Post, PostComment, PostCommentLike, PostLike


@admin.register(Post)
class PostAdmin(CustomModelAdmin):
    list_display = (
        'pkid',
        'uuid',
        'created_at',
        'updated_at',
        'is_active',
        'created_by',
        'updated_by',
        'title',
        'body',
        'author',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'is_active',
        'created_by',
        'updated_by',
        'author',
    )
    date_hierarchy = 'created_at'


@admin.register(PostComment)
class PostCommentAdmin(CustomModelAdmin):
    list_display = (
        'pkid',
        'uuid',
        'created_at',
        'updated_at',
        'is_active',
        'created_by',
        'updated_by',
        'author',
        'body',
        'post',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'is_active',
        'created_by',
        'updated_by',
        'author',
        'post',
    )
    date_hierarchy = 'created_at'


@admin.register(PostLike)
class PostLikeAdmin(CustomModelAdmin):
    list_display = (
        'pkid',
        'uuid',
        'created_at',
        'updated_at',
        'is_active',
        'created_by',
        'updated_by',
        'user',
        'post',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'is_active',
        'created_by',
        'updated_by',
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
        'is_active',
        'created_by',
        'updated_by',
        'user',
        'comment',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'is_active',
        'created_by',
        'updated_by',
        'user',
        'comment',
    )
    date_hierarchy = 'created_at'
