"""
Review serializers for API endpoints.
"""
from rest_framework import serializers
from django.db import transaction
from .models import ModelReview, ReviewVote
from users.serializers import UserSerializer
from ai_models.serializers import AIModelListSerializer


class ModelReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating model reviews.
    """
    class Meta:
        model = ModelReview
        fields = ['model', 'rating', 'review_title', 'review_text']
    
    def create(self, validated_data):
        """Create review for current user."""
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
    
    def validate(self, attrs):
        """Validate review creation."""
        user = self.context['request'].user
        model = attrs['model']
        
        # Check if user already reviewed this model
        if ModelReview.objects.filter(user=user, model=model).exists():
            raise serializers.ValidationError("You have already reviewed this model.")
        
        # Check if user has actually used the model
        from user_history.models import UserHistory
        if not UserHistory.objects.filter(user=user, model=model, response_status='success').exists():
            raise serializers.ValidationError("You must use the model before reviewing it.")
        
        return attrs


class ModelReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for model review details.
    """
    user = UserSerializer(read_only=True)
    model = AIModelListSerializer(read_only=True)
    helpfulness_ratio = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    
    class Meta:
        model = ModelReview
        fields = [
            'id', 'user', 'model', 'rating', 'review_title', 'review_text',
            'is_verified_user', 'is_approved', 'helpful_votes', 'total_votes',
            'helpfulness_ratio', 'user_vote', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'is_verified_user', 'is_approved',
            'helpful_votes', 'total_votes', 'created_at', 'updated_at'
        ]
    
    def get_helpfulness_ratio(self, obj):
        """Get helpfulness ratio."""
        return round(obj.helpfulness_ratio, 1)
    
    def get_user_vote(self, obj):
        """Get current user's vote on this review."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                vote = ReviewVote.objects.get(review=obj, user=request.user)
                return vote.vote_type
            except ReviewVote.DoesNotExist:
                pass
        return None


class ModelReviewListSerializer(serializers.ModelSerializer):
    """
    Serializer for model review list.
    """
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    helpfulness_ratio = serializers.SerializerMethodField()
    
    class Meta:
        model = ModelReview
        fields = [
            'id', 'user_name', 'rating', 'review_title', 'review_text',
            'is_verified_user', 'helpful_votes', 'total_votes',
            'helpfulness_ratio', 'created_at'
        ]
    
    def get_helpfulness_ratio(self, obj):
        """Get helpfulness ratio."""
        return round(obj.helpfulness_ratio, 1)


class ModelReviewUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating model reviews.
    """
    class Meta:
        model = ModelReview
        fields = ['rating', 'review_title', 'review_text']


class ReviewVoteSerializer(serializers.ModelSerializer):
    """
    Serializer for review votes.
    """
    class Meta:
        model = ReviewVote
        fields = ['review', 'vote_type']
    
    def create(self, validated_data):
        """Create or update vote for current user."""
        user = self.context['request'].user
        review = validated_data['review']
        vote_type = validated_data['vote_type']
        
        # Use get_or_create to handle existing votes
        vote, created = ReviewVote.objects.get_or_create(
            review=review,
            user=user,
            defaults={'vote_type': vote_type}
        )
        
        if not created and vote.vote_type != vote_type:
            # Update existing vote
            vote.vote_type = vote_type
            vote.save()
        
        return vote
    
    def validate(self, attrs):
        """Validate vote creation."""
        user = self.context['request'].user
        review = attrs['review']
        
        # Users cannot vote on their own reviews
        if review.user == user:
            raise serializers.ValidationError("You cannot vote on your own review.")
        
        return attrs


class ReviewStatsSerializer(serializers.Serializer):
    """
    Serializer for review statistics.
    """
    total_reviews = serializers.IntegerField()
    average_rating = serializers.FloatField()
    rating_distribution = serializers.DictField()
    verified_reviews_count = serializers.IntegerField()
    verified_reviews_percentage = serializers.FloatField()
    most_helpful_review = serializers.DictField()
    recent_reviews_count = serializers.IntegerField()


class UserReviewStatsSerializer(serializers.Serializer):
    """
    Serializer for user review statistics.
    """
    total_reviews_written = serializers.IntegerField()
    average_rating_given = serializers.FloatField()
    verified_reviews_count = serializers.IntegerField()
    total_helpful_votes_received = serializers.IntegerField()
    most_helpful_review = serializers.DictField()
    reviews_this_month = serializers.IntegerField()
