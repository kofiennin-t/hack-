"""
API Logs serializers for API endpoints.
"""
from rest_framework import serializers
from .models import APIUsageLog, APIMetrics
from users.serializers import UserSerializer
from developers.serializers import DeveloperListSerializer
from ai_models.serializers import AIModelListSerializer


class APIUsageLogSerializer(serializers.ModelSerializer):
    """
    Serializer for API usage log details.
    """
    user = UserSerializer(read_only=True)
    developer = DeveloperListSerializer(read_only=True)
    model = AIModelListSerializer(read_only=True)
    is_successful = serializers.SerializerMethodField()
    is_client_error = serializers.SerializerMethodField()
    is_server_error = serializers.SerializerMethodField()
    total_size_bytes = serializers.SerializerMethodField()
    
    class Meta:
        model = APIUsageLog
        fields = [
            'id', 'user', 'developer', 'model', 'api_key_used',
            'request_method', 'request_path', 'request_params',
            'response_status_code', 'request_size_bytes', 'response_size_bytes',
            'total_size_bytes', 'processing_time_ms', 'ip_address',
            'user_agent', 'referer', 'api_version', 'error_message',
            'error_code', 'is_successful', 'is_client_error',
            'is_server_error', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_is_successful(self, obj):
        """Check if request was successful."""
        return obj.is_successful
    
    def get_is_client_error(self, obj):
        """Check if there was a client error."""
        return obj.is_client_error
    
    def get_is_server_error(self, obj):
        """Check if there was a server error."""
        return obj.is_server_error
    
    def get_total_size_bytes(self, obj):
        """Get total size in bytes."""
        return obj.total_size_bytes


class APIUsageLogListSerializer(serializers.ModelSerializer):
    """
    Serializer for API usage log list (minimal data).
    """
    user_name = serializers.CharField(source='user.username', read_only=True)
    model_name = serializers.CharField(source='model.name', read_only=True)
    is_successful = serializers.SerializerMethodField()
    
    class Meta:
        model = APIUsageLog
        fields = [
            'id', 'user_name', 'model_name', 'request_method',
            'response_status_code', 'processing_time_ms',
            'is_successful', 'created_at'
        ]
    
    def get_is_successful(self, obj):
        """Check if request was successful."""
        return obj.is_successful


class APIUsageLogCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating API usage logs.
    """
    class Meta:
        model = APIUsageLog
        fields = [
            'model', 'api_key_used', 'request_method', 'request_path',
            'request_params', 'request_headers', 'response_status_code',
            'response_headers', 'request_size_bytes', 'response_size_bytes',
            'processing_time_ms', 'ip_address', 'user_agent', 'referer',
            'api_version', 'error_message', 'error_code'
        ]


class APIMetricsSerializer(serializers.ModelSerializer):
    """
    Serializer for API metrics.
    """
    model = AIModelListSerializer(read_only=True)
    developer = DeveloperListSerializer(read_only=True)
    success_rate = serializers.SerializerMethodField()
    error_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = APIMetrics
        fields = [
            'id', 'period_type', 'period_start', 'period_end',
            'model', 'developer', 'total_requests', 'successful_requests',
            'failed_requests', 'success_rate', 'error_rate',
            'average_response_time_ms', 'min_response_time_ms',
            'max_response_time_ms', 'total_data_transferred_bytes',
            'average_request_size_bytes', 'average_response_size_bytes',
            'unique_users', 'unique_ip_addresses', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_success_rate(self, obj):
        """Get success rate percentage."""
        return round(obj.success_rate, 2)
    
    def get_error_rate(self, obj):
        """Get error rate percentage."""
        return round(obj.error_rate, 2)


class APIStatsSerializer(serializers.Serializer):
    """
    Serializer for general API statistics.
    """
    total_requests = serializers.IntegerField()
    successful_requests = serializers.IntegerField()
    failed_requests = serializers.IntegerField()
    success_rate = serializers.FloatField()
    error_rate = serializers.FloatField()
    average_response_time = serializers.FloatField()
    total_data_transferred = serializers.IntegerField()
    unique_users = serializers.IntegerField()
    unique_models = serializers.IntegerField()
    requests_today = serializers.IntegerField()
    requests_this_month = serializers.IntegerField()
    top_models = serializers.ListField()
    error_distribution = serializers.DictField()


class DeveloperAPIStatsSerializer(serializers.Serializer):
    """
    Serializer for developer-specific API statistics.
    """
    total_requests = serializers.IntegerField()
    successful_requests = serializers.IntegerField()
    failed_requests = serializers.IntegerField()
    success_rate = serializers.FloatField()
    average_response_time = serializers.FloatField()
    total_data_transferred = serializers.IntegerField()
    unique_users = serializers.IntegerField()
    requests_today = serializers.IntegerField()
    requests_this_month = serializers.IntegerField()
    top_performing_models = serializers.ListField()
    recent_errors = serializers.ListField()


class ModelAPIStatsSerializer(serializers.Serializer):
    """
    Serializer for model-specific API statistics.
    """
    total_requests = serializers.IntegerField()
    successful_requests = serializers.IntegerField()
    failed_requests = serializers.IntegerField()
    success_rate = serializers.FloatField()
    average_response_time = serializers.FloatField()
    total_data_transferred = serializers.IntegerField()
    unique_users = serializers.IntegerField()
    requests_today = serializers.IntegerField()
    requests_this_month = serializers.IntegerField()
    hourly_distribution = serializers.DictField()
    status_code_distribution = serializers.DictField()
    recent_performance_trend = serializers.ListField()
