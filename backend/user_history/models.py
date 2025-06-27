"""
User History models for tracking AI model interactions.
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import BaseModel
from users.models import User


class UserHistory(BaseModel):
    """
    Track user interactions with AI models.
    """
    RESPONSE_STATUS_CHOICES = [
        ('success', 'Success'),
        ('error', 'Error'),
        ('timeout', 'Timeout'),
        ('rate_limited', 'Rate Limited'),
        ('insufficient_quota', 'Insufficient Quota'),
    ]
    
    # Core relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    model = models.ForeignKey('ai_models.AIModel', on_delete=models.CASCADE, related_name='usage_history')
    
    # Session and request details
    session_id = models.CharField(max_length=255, db_index=True)
    request_id = models.UUIDField(default=uuid.uuid4, unique=True)
    
    # Request content
    prompt = models.TextField()
    request_parameters = models.JSONField(default=dict, blank=True)
    
    # Response content
    response = models.TextField(blank=True)
    response_status = models.CharField(max_length=20, choices=RESPONSE_STATUS_CHOICES, default='success')
    response_timestamp = models.DateTimeField(auto_now_add=True)
    
    # Performance metrics
    response_time_ms = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Response time in milliseconds"
    )
    
    # Token usage (for token-based pricing)
    input_tokens = models.PositiveIntegerField(default=0)
    output_tokens = models.PositiveIntegerField(default=0)
    
    # Cost tracking
    cost_incurred = models.DecimalField(max_digits=10, decimal_places=6, default=0.000000)
    
    # User feedback
    user_rating = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="User rating from 1-5 stars"
    )
    user_feedback = models.TextField(blank=True)
    
    # Technical details
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    api_version = models.CharField(max_length=20, default='v1')
    
    class Meta:
        db_table = 'user_history'
        verbose_name = 'User History'
        verbose_name_plural = 'User Histories'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['model']),
            models.Index(fields=['session_id']),
            models.Index(fields=['response_status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['user', 'model']),
            models.Index(fields=['user', 'session_id']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.model.name} ({self.created_at})"
    
    def calculate_cost(self):
        """Calculate cost based on model pricing."""
        model = self.model
        
        if model.pricing_type == 'per_request':
            self.cost_incurred = model.price_per_request
        elif model.pricing_type == 'per_token':
            total_tokens = self.input_tokens + self.output_tokens
            self.cost_incurred = model.price_per_token * total_tokens
        elif model.pricing_type == 'free':
            self.cost_incurred = 0.0
        # For subscription models, cost is handled elsewhere
        
        return self.cost_incurred
    
    def save(self, *args, **kwargs):
        # Calculate cost if not already set
        if self.cost_incurred == 0 and self.model.pricing_type in ['per_request', 'per_token']:
            self.calculate_cost()
        
        super().save(*args, **kwargs)
        
        # Update model metrics
        if self.response_status == 'success':
            self.model.increment_request_count()
            self.model.update_average_response_time(self.response_time_ms)
            self.model.update_success_rate(True)
            
            # Add revenue to developer
            if self.cost_incurred > 0:
                self.model.developer.add_revenue(self.cost_incurred)
        else:
            self.model.update_success_rate(False)
    
    @property
    def total_tokens(self):
        """Get total tokens used."""
        return self.input_tokens + self.output_tokens
    
    @property
    def is_successful(self):
        """Check if the interaction was successful."""
        return self.response_status == 'success'
