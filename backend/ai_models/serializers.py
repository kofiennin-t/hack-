"""
AI Model serializers for API endpoints.
"""
from rest_framework import serializers
from .models import AIModel
from developers.serializers import DeveloperListSerializer


class AIModelCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating AI models.
    """
    class Meta:
        model = AIModel
        fields = [
            'name', 'description', 'category', 'api_name', 'api_endpoint',
            'api_version', 'tags', 'thumbnail_url', 'documentation_url',
            'example_request', 'example_response', 'pricing_type',
            'price_per_request', 'price_per_token', 'monthly_subscription_price',
            'rate_limit_per_minute', 'rate_limit_per_hour', 'rate_limit_per_day',
            'max_tokens', 'supported_languages', 'is_public'
        ]
    
    def create(self, validated_data):
        """Create model for current developer."""
        developer = self.context['request'].user.developer_profile
        validated_data['developer'] = developer
        return super().create(validated_data)


class AIModelSerializer(serializers.ModelSerializer):
    """
    Serializer for AI model details.
    """
    developer = DeveloperListSerializer(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    pricing_type_display = serializers.CharField(source='get_pricing_type_display', read_only=True)
    
    class Meta:
        model = AIModel
        fields = [
            'id', 'developer', 'name', 'description', 'category', 'category_display',
            'api_name', 'api_endpoint', 'api_version', 'tags', 'thumbnail_url',
            'documentation_url', 'example_request', 'example_response',
            'pricing_type', 'pricing_type_display', 'price_per_request',
            'price_per_token', 'monthly_subscription_price', 'rate_limit_per_minute',
            'rate_limit_per_hour', 'rate_limit_per_day', 'max_tokens',
            'supported_languages', 'status', 'status_display', 'is_public',
            'total_requests', 'average_response_time', 'success_rate',
            'average_rating', 'total_reviews', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'developer', 'total_requests', 'average_response_time',
            'success_rate', 'average_rating', 'total_reviews',
            'created_at', 'updated_at'
        ]


class AIModelListSerializer(serializers.ModelSerializer):
    """
    Serializer for AI model list (public view).
    """
    developer_name = serializers.CharField(source='developer.developer_name', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    pricing_type_display = serializers.CharField(source='get_pricing_type_display', read_only=True)
    
    class Meta:
        model = AIModel
        fields = [
            'id', 'name', 'description', 'category', 'category_display',
            'api_name', 'tags', 'thumbnail_url', 'pricing_type',
            'pricing_type_display', 'price_per_request', 'price_per_token',
            'monthly_subscription_price', 'status', 'is_public',
            'average_rating', 'total_reviews', 'total_requests',
            'developer_name', 'created_at'
        ]


class AIModelUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating AI models.
    """
    class Meta:
        model = AIModel
        fields = [
            'name', 'description', 'tags', 'thumbnail_url', 'documentation_url',
            'example_request', 'example_response', 'pricing_type',
            'price_per_request', 'price_per_token', 'monthly_subscription_price',
            'rate_limit_per_minute', 'rate_limit_per_hour', 'rate_limit_per_day',
            'max_tokens', 'supported_languages', 'status', 'is_public'
        ]


class AIModelStatsSerializer(serializers.Serializer):
    """
    Serializer for AI model statistics.
    """
    total_requests = serializers.IntegerField()
    total_interactions = serializers.IntegerField()
    unique_users = serializers.IntegerField()
    average_response_time = serializers.FloatField()
    success_rate = serializers.FloatField()
    average_rating = serializers.FloatField()
    total_reviews = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    requests_today = serializers.IntegerField()
    requests_this_month = serializers.IntegerField()


class AIModelSearchSerializer(serializers.ModelSerializer):
    """
    Serializer for AI model search results.
    """
    developer_name = serializers.CharField(source='developer.developer_name', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = AIModel
        fields = [
            'id', 'name', 'description', 'category', 'category_display',
            'api_name', 'tags', 'thumbnail_url', 'average_rating',
            'total_reviews', 'pricing_type', 'price_per_request',
            'developer_name', 'is_public', 'status'
        ]
