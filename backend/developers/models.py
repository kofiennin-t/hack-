"""
Developer models for managing AI model creators.
"""
import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from core.models import BaseModel
from users.models import User


class Developer(BaseModel):
    """
    Developer model for AI model creators.
    """
    DEVELOPER_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('pending_approval', 'Pending Approval'),
    ]
    
    # Link to user account
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='developer_profile')
    
    # Developer specific information
    developer_name = models.CharField(max_length=100, unique=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    
    # Contact information
    business_email = models.EmailField(blank=True, null=True)
    business_phone = PhoneNumberField(blank=True, null=True)
    
    # Professional details
    specialization = ArrayField(
        models.CharField(max_length=100),
        size=10,
        default=list,
        help_text="Areas of AI/ML specialization"
    )
    bio = models.TextField(blank=True)
    years_experience = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    
    # Status and verification
    status = models.CharField(max_length=20, choices=DEVELOPER_STATUS_CHOICES, default='pending_approval')
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    
    # API and quota management
    api_key = models.CharField(max_length=255, unique=True, blank=True, null=True)
    monthly_quota_limit = models.PositiveIntegerField(default=10000)
    current_month_usage = models.PositiveIntegerField(default=0)
    
    # Revenue tracking
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        db_table = 'developers'
        verbose_name = 'Developer'
        verbose_name_plural = 'Developers'
        indexes = [
            models.Index(fields=['developer_name']),
            models.Index(fields=['status']),
            models.Index(fields=['is_verified']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.developer_name} ({self.user.email})"
    
    def save(self, *args, **kwargs):
        # Generate API key if not exists
        if not self.api_key:
            import secrets
            self.api_key = f"dev_{secrets.token_urlsafe(32)}"
        super().save(*args, **kwargs)
    
    def is_quota_available(self, requested_calls=1):
        """Check if developer has quota available."""
        return (self.current_month_usage + requested_calls) <= self.monthly_quota_limit
    
    def increment_usage(self, calls=1):
        """Increment API usage count."""
        self.current_month_usage += calls
        self.save(update_fields=['current_month_usage'])
    
    def reset_monthly_usage(self):
        """Reset monthly usage counter."""
        self.current_month_usage = 0
        self.save(update_fields=['current_month_usage'])
    
    def add_revenue(self, amount):
        """Add revenue to developer's total."""
        self.total_revenue += amount
        self.save(update_fields=['total_revenue'])
