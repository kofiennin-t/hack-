"""
User History serializers for API endpoints.
"""
from rest_framework import serializers
from .models import UserHistory
from users.serializers import UserSerializer
from ai_models.serializers import AIModelListSerializer


class UserHistoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating user history entries.
    """
    class Meta:
        model = UserHistory
        fields = [
            'model', 'session_id', 'prompt', 'request_parameters',
            'response', 'response_status', 'response_time_ms',
            'input_tokens', 'output_tokens', 'user_rating',
            'user_feedback', 'ip_address', 'user_agent', 'api_version'
        ]
    
    def create(self, validated_data):
        """Create history entry for current user."""
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class UserHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for user history details.
    """
    user = UserSerializer(read_only=True)
    model = AIModelListSerializer(read_only=True)
    response_status_display = serializers.CharField(source='get_response_status_display', read_only=True)
    total_tokens = serializers.SerializerMethodField()
    is_successful = serializers.SerializerMethodField()
    
    class Meta:
        model = UserHistory
        fields = [
            'id', 'user', 'model', 'session_id', 'request_id',
            'prompt', 'request_parameters', 'response', 'response_status',
            'response_status_display', 'response_timestamp', 'response_time_ms',
            'input_tokens', 'output_tokens', 'total_tokens', 'cost_incurred',
            'user_rating', 'user_feedback', 'ip_address', 'user_agent',
            'api_version', 'is_successful', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'request_id', 'response_timestamp',
            'cost_incurred', 'created_at', 'updated_at'
        ]
    
    def get_total_tokens(self, obj):
        """Get total tokens used."""
        return obj.total_tokens
    
    def get_is_successful(self, obj):
        """Check if interaction was successful."""
        return obj.is_successful


class UserHistoryListSerializer(serializers.ModelSerializer):
    """
    Serializer for user history list (minimal data).
    """
    model_name = serializers.CharField(source='model.name', read_only=True)
    response_status_display = serializers.CharField(source='get_response_status_display', read_only=True)
    total_tokens = serializers.SerializerMethodField()
    
    class Meta:
        model = UserHistory
        fields = [
            'id', 'model_name', 'session_id', 'response_status',
            'response_status_display', 'response_time_ms', 'total_tokens',
            'cost_incurred', 'user_rating', 'created_at'
        ]
    
    def get_total_tokens(self, obj):
        """Get total tokens used."""
        return obj.total_tokens


class UserHistoryUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user history (mainly for rating/feedback).
    """
    class Meta:
        model = UserHistory
        fields = ['user_rating', 'user_feedback']
    
    def validate_user_rating(self, value):
        """Validate user rating."""
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class UserHistoryStatsSerializer(serializers.Serializer):
    """
    Serializer for user history statistics.
    """
    total_interactions = serializers.IntegerField()
    unique_models = serializers.IntegerField()
    unique_sessions = serializers.IntegerField()
    average_rating = serializers.FloatField()
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=6)
    average_response_time = serializers.FloatField()
    success_rate = serializers.FloatField()
    total_tokens = serializers.IntegerField()
    most_used_model = serializers.CharField()
    interactions_today = serializers.IntegerField()
    interactions_this_month = serializers.IntegerField()


class SessionStatsSerializer(serializers.Serializer):
    """
    Serializer for session statistics.
    """
    session_id = serializers.CharField()
    interaction_count = serializers.IntegerField()
    first_interaction = serializers.DateTimeField()
    last_interaction = serializers.DateTimeField()
    unique_models = serializers.IntegerField()
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=6)
    average_response_time = serializers.FloatField()
