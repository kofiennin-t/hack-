"""
Developer serializers for API endpoints.
"""
from rest_framework import serializers
from .models import Developer
from users.serializers import UserSerializer


class DeveloperRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for developer registration.
    """
    class Meta:
        model = Developer
        fields = [
            'developer_name', 'company_name', 'website_url', 'business_email',
            'business_phone', 'specialization', 'bio', 'years_experience'
        ]
    
    def create(self, validated_data):
        """Create developer profile for current user."""
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class DeveloperSerializer(serializers.ModelSerializer):
    """
    Serializer for developer details.
    """
    user = UserSerializer(read_only=True)
    quota_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Developer
        fields = [
            'id', 'user', 'developer_name', 'company_name', 'website_url',
            'business_email', 'business_phone', 'specialization', 'bio',
            'years_experience', 'status', 'is_verified', 'verification_date',
            'monthly_quota_limit', 'current_month_usage', 'quota_percentage',
            'total_revenue', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'status', 'is_verified', 'verification_date',
            'api_key', 'current_month_usage', 'total_revenue',
            'created_at', 'updated_at'
        ]
    
    def get_quota_percentage(self, obj):
        """Calculate quota usage percentage."""
        if obj.monthly_quota_limit == 0:
            return 0
        return (obj.current_month_usage / obj.monthly_quota_limit) * 100


class DeveloperListSerializer(serializers.ModelSerializer):
    """
    Serializer for developer list (public view).
    """
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    model_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Developer
        fields = [
            'id', 'developer_name', 'company_name', 'website_url',
            'specialization', 'bio', 'years_experience',
            'is_verified', 'user_name', 'user_email', 'model_count', 'created_at'
        ]
    
    def get_model_count(self, obj):
        """Get number of models by developer."""
        return obj.models.filter(status='active').count()


class DeveloperUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating developer profile.
    """
    class Meta:
        model = Developer
        fields = [
            'developer_name', 'company_name', 'website_url', 'business_email',
            'business_phone', 'specialization', 'bio', 'years_experience'
        ]


class DeveloperStatsSerializer(serializers.Serializer):
    """
    Serializer for developer statistics.
    """
    total_models = serializers.IntegerField()
    active_models = serializers.IntegerField()
    total_interactions = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    avg_model_rating = serializers.FloatField()
    current_month_usage = serializers.IntegerField()
    quota_limit = serializers.IntegerField()
    quota_percentage = serializers.FloatField()
