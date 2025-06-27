"""
Django admin configuration for Developers app.
"""
from django.contrib import admin
from .models import Developer


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    """Admin interface for Developer model."""
    
    list_display = (
        'developer_name', 'user_email', 'company_name', 
        'status', 'is_verified', 'monthly_quota_limit', 
        'current_month_usage', 'total_revenue', 'created_at'
    )
    list_filter = ('status', 'is_verified', 'specialization', 'created_at')
    search_fields = (
        'developer_name', 'company_name', 'user__email', 
        'user__username', 'specialization'
    )
    ordering = ('-created_at',)
    readonly_fields = ('api_key', 'total_revenue', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'developer_name', 'company_name', 'website_url')
        }),
        ('Contact Information', {
            'fields': ('business_email', 'business_phone')
        }),
        ('Professional Details', {
            'fields': ('specialization', 'bio', 'years_experience')
        }),
        ('Status & Verification', {
            'fields': ('status', 'is_verified', 'verification_date')
        }),
        ('API & Quota Management', {
            'fields': ('api_key', 'monthly_quota_limit', 'current_month_usage')
        }),
        ('Revenue Tracking', {
            'fields': ('total_revenue',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
    user_email.admin_order_field = 'user__email'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    actions = ['verify_developers', 'reset_monthly_usage']
    
    def verify_developers(self, request, queryset):
        """Verify selected developers."""
        from django.utils import timezone
        queryset.update(is_verified=True, verification_date=timezone.now(), status='active')
        self.message_user(request, f"{queryset.count()} developers verified successfully.")
    verify_developers.short_description = "Verify selected developers"
    
    def reset_monthly_usage(self, request, queryset):
        """Reset monthly usage for selected developers."""
        queryset.update(current_month_usage=0)
        self.message_user(request, f"Monthly usage reset for {queryset.count()} developers.")
