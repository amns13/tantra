# -*- coding: utf-8 -*-
from core.admin import CustomModelAdmin
from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(CustomModelAdmin):
    list_display = (
        'password',
        'last_login',
        'is_superuser',
        'pkid',
        'uuid',
        'created_at',
        'updated_at',
        'is_active',
        'created_by',
        'updated_by',
        'username',
        'email',
        'is_staff',
    )
    list_filter = (
        'last_login',
        'is_superuser',
        'created_at',
        'updated_at',
        'is_active',
        'created_by',
        'updated_by',
        'is_staff',
    )
    raw_id_fields = ('groups', 'user_permissions')
    date_hierarchy = 'created_at'
