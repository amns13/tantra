# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from core.admin import CustomModelAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(CustomModelAdmin, UserAdmin):
    list_display = (
        'pkid',
        'username',
        'email',
        'uuid',
        'is_staff',
        'is_verified',
        'is_superuser',
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )
    list_filter = (
        'is_superuser',
        'is_active',
        'is_staff',
        'is_verified',
    )
    raw_id_fields = ('groups', 'user_permissions')
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email')
    filter_horizontal = ('groups', 'user_permissions',)
