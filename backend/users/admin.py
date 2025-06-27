"""
Django admin configuration for Users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""
    
    list_display = (
        'username', 'email', 'first_name', 'last_name', 
        'status', 'email_verified', 'is_staff', 'date_joined'
    )
    list_filter = (
        'status', 'email_verified', 'is_staff', 'is_superuser', 
        'is_active', 'date_joined'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': (
                'date_of_birth', 'phone_number', 'country', 'city',
                'profile_picture_url', 'bio'
            )
        }),
        ('Status & Verification', {
            'fields': (
                'status', 'email_verified', 'email_verification_token',
                'password_reset_token', 'password_reset_expires'
            )
        }),
        ('Activity Tracking', {
            'fields': ('last_login', 'login_count')
        }),
    )
    
    readonly_fields = ('login_count', 'date_joined', 'last_login')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
