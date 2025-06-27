"""
AI Model models for the platform.
"""
import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import BaseModel
from developers.models import Developer


class AIModel(BaseModel):
    """
    AI Model representation.
    """
    MODEL_CATEGORY_CHOICES = [
        ('nlp', 'Natural Language Processing'),
        ('computer_vision', 'Computer Vision'),
        ('speech', 'Speech & Audio'),
        ('recommendation', 'Recommendation Systems'),
        ('forecasting', 'Forecasting & Prediction'),
        ('classification', 'Classification'),
        ('generation', 'Content Generation'),
        ('translation', 'Translation'),
        ('sentiment', 'Sentiment Analysis'),
        ('other', 'Other'),
    ]
    
    MODEL_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deprecated', 'Deprecated'),
        ('beta', 'Beta'),
        ('maintenance', 'Under Maintenance'),
    ]
    
    PRICING_TYPE_CHOICES = [
        ('per_request', 'Per Request'),
        ('per_token', 'Per Token'),
        ('subscription', 'Subscription'),
        ('free', 'Free'),
    ]
    
    # Basic information
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=MODEL_CATEGORY_CHOICES)
    
    # API details
    api_name = models.CharField(max_length=100, unique=True)
    api_endpoint = models.URLField()
    api_version = models.CharField(max_length=20, default='v1')
    
    # Model metadata
    tags = ArrayField(
        models.CharField(max_length=50),
        size=20,
        default=list,
        help_text="Tags for categorization and search"
    )
    
    # Visual and documentation
    thumbnail_url = models.URLField(blank=True, null=True)
    documentation_url = models.URLField(blank=True, null=True)
    example_request = JSONField(default=dict, blank=True)
    example_response = JSONField(default=dict, blank=True)
    
    # Pricing and limits
    pricing_type = models.CharField(max_length=20, choices=PRICING_TYPE_CHOICES, default='per_request')
    price_per_request = models.DecimalField(max_digits=10, decimal_places=4, default=0.0001)
    price_per_token = models.DecimalField(max_digits=10, decimal_places=6, default=0.000001)
    monthly_subscription_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Rate limiting
    rate_limit_per_minute = models.PositiveIntegerField(default=60)
    rate_limit_per_hour = models.PositiveIntegerField(default=1000)
    rate_limit_per_day = models.PositiveIntegerField(default=10000)
    
    # Model specifications
    max_tokens = models.PositiveIntegerField(null=True, blank=True)
    supported_languages = ArrayField(
        models.CharField(max_length=10),
        size=50,
        default=list,
        help_text="Supported language codes (e.g., 'en', 'es', 'fr')"
    )
    
    # Status and metrics
    status = models.CharField(max_length=20, choices=MODEL_STATUS_CHOICES, default='active')
    is_public = models.BooleanField(default=True)
    
    # Performance metrics (updated by system)
    total_requests = models.PositiveIntegerField(default=0)
    average_response_time = models.FloatField(default=0.0)  # in milliseconds
    success_rate = models.FloatField(default=100.0)  # percentage
    
    # Rating and reviews
    average_rating = models.FloatField(default=0.0)
    total_reviews = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'models'
        verbose_name = 'AI Model'
        verbose_name_plural = 'AI Models'
        indexes = [
            models.Index(fields=['api_name']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['is_public']),
            models.Index(fields=['developer']),
            models.Index(fields=['created_at']),
            models.Index(fields=['average_rating']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(average_rating__gte=0, average_rating__lte=5),
                name='valid_rating_range'
            ),
            models.CheckConstraint(
                check=models.Q(success_rate__gte=0, success_rate__lte=100),
                name='valid_success_rate'
            ),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.api_name})"
    
    def increment_request_count(self):
        """Increment total request count."""
        self.total_requests += 1
        self.save(update_fields=['total_requests'])
    
    def update_average_response_time(self, new_response_time):
        """Update average response time with new measurement."""
        if self.total_requests == 0:
            self.average_response_time = new_response_time
        else:
            # Calculate rolling average
            current_total = self.average_response_time * (self.total_requests - 1)
            self.average_response_time = (current_total + new_response_time) / self.total_requests
        
        self.save(update_fields=['average_response_time'])
    
    def update_success_rate(self, was_successful):
        """Update success rate based on request outcome."""
        if self.total_requests <= 1:
            self.success_rate = 100.0 if was_successful else 0.0
        else:
            # Calculate new success rate
            current_successful = (self.success_rate / 100.0) * (self.total_requests - 1)
            if was_successful:
                current_successful += 1
            
            self.success_rate = (current_successful / self.total_requests) * 100.0
        
        self.save(update_fields=['success_rate'])
    
    def update_rating(self):
        """Update average rating from reviews."""
        from reviews.models import ModelReview
        reviews = ModelReview.objects.filter(model=self)
        
        if reviews.exists():
            from django.db.models import Avg
            avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
            self.average_rating = round(avg_rating, 2)
            self.total_reviews = reviews.count()
        else:
            self.average_rating = 0.0
            self.total_reviews = 0
        
        self.save(update_fields=['average_rating', 'total_reviews'])
    
    def is_rate_limited(self, user, time_window='minute'):
        """Check if user has exceeded rate limits."""
        from user_history.models import UserHistory
        from django.utils import timezone
        from datetime import timedelta
        
        # Define time windows
        if time_window == 'minute':
            since = timezone.now() - timedelta(minutes=1)
            limit = self.rate_limit_per_minute
        elif time_window == 'hour':
            since = timezone.now() - timedelta(hours=1)
            limit = self.rate_limit_per_hour
        elif time_window == 'day':
            since = timezone.now() - timedelta(days=1)
            limit = self.rate_limit_per_day
        else:
            return False
        
        # Count recent requests
        recent_requests = UserHistory.objects.filter(
            user=user,
            model=self,
            created_at__gte=since
        ).count()
        
        return recent_requests >= limit
