"""
API Usage Log models for tracking platform usage.
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from core.models import BaseModel
from users.models import User
from developers.models import Developer


class APIUsageLog(BaseModel):
    """
    Track API usage across the platform.
    """
    REQUEST_METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE'),
    ]
    
    # Optional relationships (can be null for anonymous access)
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='api_logs'
    )
    developer = models.ForeignKey(
        Developer, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='api_logs'
    )
    model = models.ForeignKey(
        'ai_models.AIModel', 
        on_delete=models.CASCADE, 
        related_name='api_logs'
    )
    
    # Request details
    api_key_used = models.CharField(max_length=255, blank=True, null=True)
    request_method = models.CharField(max_length=10, choices=REQUEST_METHOD_CHOICES)
    request_path = models.TextField()
    request_params = models.JSONField(default=dict, blank=True)
    request_headers = models.JSONField(default=dict, blank=True)
    
    # Response details
    response_status_code = models.PositiveIntegerField()
    response_headers = models.JSONField(default=dict, blank=True)
    
    # Performance and size metrics
    request_size_bytes = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    response_size_bytes = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    processing_time_ms = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Total processing time in milliseconds"
    )
    
    # Network and client information
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    referer = models.URLField(blank=True, null=True)
    
    # API versioning
    api_version = models.CharField(max_length=20, default='v1')
    
    # Error tracking
    error_message = models.TextField(blank=True, null=True)
    error_code = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        db_table = 'api_usage_logs'
        verbose_name = 'API Usage Log'
        verbose_name_plural = 'API Usage Logs'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['developer']),
            models.Index(fields=['model']),
            models.Index(fields=['api_key_used']),
            models.Index(fields=['request_method']),
            models.Index(fields=['response_status_code']),
            models.Index(fields=['created_at']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['api_version']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        user_info = self.user.username if self.user else "Anonymous"
        return f"{user_info} - {self.request_method} {self.model.name} ({self.response_status_code})"
    
    @property
    def is_successful(self):
        """Check if the API call was successful."""
        return 200 <= self.response_status_code < 300
    
    @property
    def is_client_error(self):
        """Check if there was a client error."""
        return 400 <= self.response_status_code < 500
    
    @property
    def is_server_error(self):
        """Check if there was a server error."""
        return self.response_status_code >= 500
    
    @property
    def total_size_bytes(self):
        """Get total request + response size."""
        return self.request_size_bytes + self.response_size_bytes
    
    def save(self, *args, **kwargs):
        # Set developer from model if not provided
        if not self.developer and self.model:
            self.developer = self.model.developer
        
        super().save(*args, **kwargs)


class APIMetrics(BaseModel):
    """
    Aggregated API metrics for performance monitoring.
    """
    METRIC_PERIOD_CHOICES = [
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    # Time period
    period_type = models.CharField(max_length=20, choices=METRIC_PERIOD_CHOICES)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    
    # Optional grouping
    model = models.ForeignKey(
        'ai_models.AIModel',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='metrics'
    )
    developer = models.ForeignKey(
        Developer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='metrics'
    )
    
    # Aggregated metrics
    total_requests = models.PositiveIntegerField(default=0)
    successful_requests = models.PositiveIntegerField(default=0)
    failed_requests = models.PositiveIntegerField(default=0)
    
    # Performance metrics
    average_response_time_ms = models.FloatField(default=0.0)
    min_response_time_ms = models.PositiveIntegerField(default=0)
    max_response_time_ms = models.PositiveIntegerField(default=0)
    
    # Data transfer metrics
    total_data_transferred_bytes = models.BigIntegerField(default=0)
    average_request_size_bytes = models.FloatField(default=0.0)
    average_response_size_bytes = models.FloatField(default=0.0)
    
    # User metrics
    unique_users = models.PositiveIntegerField(default=0)
    unique_ip_addresses = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'api_metrics'
        verbose_name = 'API Metrics'
        verbose_name_plural = 'API Metrics'
        unique_together = [
            ['period_type', 'period_start', 'model'],
            ['period_type', 'period_start', 'developer'],
        ]
        indexes = [
            models.Index(fields=['period_type', 'period_start']),
            models.Index(fields=['model']),
            models.Index(fields=['developer']),
        ]
        ordering = ['-period_start']
    
    def __str__(self):
        target = self.model.name if self.model else f"Developer: {self.developer.developer_name}"
        return f"{self.period_type} metrics for {target} ({self.period_start.date()})"
    
    @property
    def success_rate(self):
        """Calculate success rate percentage."""
        if self.total_requests == 0:
            return 0
        return (self.successful_requests / self.total_requests) * 100
    
    @property
    def error_rate(self):
        """Calculate error rate percentage."""
        if self.total_requests == 0:
            return 0
        return (self.failed_requests / self.total_requests) * 100
