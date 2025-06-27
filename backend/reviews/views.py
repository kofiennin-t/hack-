"""
Review views for API endpoints.
"""
from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema
from core.permissions import IsOwnerOrAdmin
from .models import ModelReview, ReviewVote
from .serializers import (
    ModelReviewSerializer,
    ModelReviewCreateSerializer,
    ModelReviewUpdateSerializer,
    ModelReviewListSerializer,
    ReviewVoteSerializer,
    ReviewStatsSerializer,
    UserReviewStatsSerializer
)


class ModelReviewViewSet(ModelViewSet):
    """
    ViewSet for managing model reviews.
    """
    queryset = ModelReview.objects.select_related('user', 'model').filter(is_approved=True)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['review_title', 'review_text']
    ordering_fields = ['created_at', 'rating', 'helpful_votes', 'total_votes']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ModelReviewCreateSerializer
        elif self.action == 'list':
            return ModelReviewListSerializer
        elif self.action in ['update', 'partial_update']:
            return ModelReviewUpdateSerializer
        return ModelReviewSerializer
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by model
        model_id = self.request.query_params.get('model')
        if model_id:
            queryset = queryset.filter(model_id=model_id)
        
        # Filter by rating
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            try:
                queryset = queryset.filter(rating__gte=int(min_rating))
            except ValueError:
                pass
        
        max_rating = self.request.query_params.get('max_rating')
        if max_rating:
            try:
                queryset = queryset.filter(rating__lte=int(max_rating))
            except ValueError:
                pass
        
        # Filter by verification status
        verified_only = self.request.query_params.get('verified_only')
        if verified_only and verified_only.lower() in ['true', '1', 'yes']:
            queryset = queryset.filter(is_verified_user=True)
        
        # Filter by helpfulness
        min_helpfulness = self.request.query_params.get('min_helpfulness')
        if min_helpfulness:
            try:
                min_help_float = float(min_helpfulness)
                # Calculate helpfulness ratio using database operations
                queryset = queryset.extra(
                    where=["(helpful_votes::float / NULLIF(total_votes, 0)) * 100 >= %s"],
                    params=[min_help_float]
                )
            except ValueError:
                pass
        
        # For user's own reviews
        if (self.request.user.is_authenticated and 
            self.action in ['update', 'partial_update', 'destroy']):
            queryset = queryset.filter(user=self.request.user)
        
        return queryset
    
    @extend_schema(
        summary="Vote on review helpfulness",
        description="Vote whether a review is helpful or not"
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def vote(self, request, pk=None):
        """Vote on review helpfulness."""
        review = self.get_object()
        
        # Check if user is trying to vote on their own review
        if review.user == request.user:
            return Response(
                {'error': 'You cannot vote on your own review'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        vote_type = request.data.get('vote_type')
        if vote_type not in ['helpful', 'not_helpful']:
            return Response(
                {'error': 'vote_type must be "helpful" or "not_helpful"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create or update vote
        data = {'review': review.id, 'vote_type': vote_type}
        serializer = ReviewVoteSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            vote = serializer.save()
            
            # Refresh review to get updated vote counts
            review.refresh_from_db()
            
            return Response({
                'message': 'Vote recorded successfully',
                'vote_type': vote.vote_type,
                'helpful_votes': review.helpful_votes,
                'total_votes': review.total_votes
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Remove vote from review",
        description="Remove your vote from a review"
    )
    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def remove_vote(self, request, pk=None):
        """Remove vote from review."""
        review = self.get_object()
        
        try:
            vote = ReviewVote.objects.get(review=review, user=request.user)
            vote.delete()
            
            # Refresh review to get updated vote counts
            review.refresh_from_db()
            
            return Response({
                'message': 'Vote removed successfully',
                'helpful_votes': review.helpful_votes,
                'total_votes': review.total_votes
            })
        
        except ReviewVote.DoesNotExist:
            return Response(
                {'error': 'You have not voted on this review'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ModelReviewStatsView(generics.RetrieveAPIView):
    """
    View for getting review statistics for a specific model.
    """
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        summary="Get model review statistics",
        description="Get comprehensive review statistics for a specific model"
    )
    def get(self, request, model_id):
        """Get review statistics for a model."""
        from ai_models.models import AIModel
        
        try:
            model = AIModel.objects.get(id=model_id)
        except AIModel.DoesNotExist:
            return Response(
                {'error': 'Model not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        reviews = ModelReview.objects.filter(model=model, is_approved=True)
        
        if not reviews.exists():
            stats_data = {
                'total_reviews': 0,
                'average_rating': 0,
                'rating_distribution': {str(i): 0 for i in range(1, 6)},
                'verified_reviews_count': 0,
                'verified_reviews_percentage': 0,
                'most_helpful_review': None,
                'recent_reviews_count': 0
            }
        else:
            # Basic statistics
            total_reviews = reviews.count()
            average_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
            
            # Rating distribution
            rating_dist = reviews.values('rating').annotate(count=Count('rating'))
            rating_distribution = {str(i): 0 for i in range(1, 6)}
            for item in rating_dist:
                rating_distribution[str(item['rating'])] = item['count']
            
            # Verified reviews
            verified_count = reviews.filter(is_verified_user=True).count()
            verified_percentage = (verified_count / total_reviews * 100) if total_reviews > 0 else 0
            
            # Most helpful review
            most_helpful = reviews.filter(total_votes__gt=0).order_by(
                '-helpful_votes', '-total_votes'
            ).first()
            
            most_helpful_data = None
            if most_helpful:
                most_helpful_data = {
                    'id': str(most_helpful.id),
                    'title': most_helpful.review_title,
                    'rating': most_helpful.rating,
                    'helpful_votes': most_helpful.helpful_votes,
                    'total_votes': most_helpful.total_votes,
                    'user_name': most_helpful.user.get_full_name()
                }
            
            # Recent reviews (last 30 days)
            thirty_days_ago = timezone.now() - timedelta(days=30)
            recent_count = reviews.filter(created_at__gte=thirty_days_ago).count()
            
            stats_data = {
                'total_reviews': total_reviews,
                'average_rating': round(average_rating, 2),
                'rating_distribution': rating_distribution,
                'verified_reviews_count': verified_count,
                'verified_reviews_percentage': round(verified_percentage, 1),
                'most_helpful_review': most_helpful_data,
                'recent_reviews_count': recent_count
            }
        
        serializer = ReviewStatsSerializer(stats_data)
        return Response(serializer.data)


class UserReviewStatsView(generics.RetrieveAPIView):
    """
    View for getting user's review statistics.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Get user review statistics",
        description="Get comprehensive review statistics for the current user"
    )
    def get(self, request):
        """Get review statistics for current user."""
        user = request.user
        reviews = ModelReview.objects.filter(user=user)
        
        if not reviews.exists():
            stats_data = {
                'total_reviews_written': 0,
                'average_rating_given': 0,
                'verified_reviews_count': 0,
                'total_helpful_votes_received': 0,
                'most_helpful_review': None,
                'reviews_this_month': 0
            }
        else:
            # Basic statistics
            total_reviews = reviews.count()
            avg_rating_given = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
            verified_count = reviews.filter(is_verified_user=True).count()
            total_helpful_votes = reviews.aggregate(total_helpful=Count('helpful_votes'))['total_helpful'] or 0
            
            # Most helpful review by this user
            most_helpful = reviews.filter(total_votes__gt=0).order_by(
                '-helpful_votes', '-total_votes'
            ).first()
            
            most_helpful_data = None
            if most_helpful:
                most_helpful_data = {
                    'id': str(most_helpful.id),
                    'title': most_helpful.review_title,
                    'model_name': most_helpful.model.name,
                    'rating': most_helpful.rating,
                    'helpful_votes': most_helpful.helpful_votes,
                    'total_votes': most_helpful.total_votes
                }
            
            # Reviews this month
            first_day_of_month = timezone.now().replace(day=1)
            reviews_this_month = reviews.filter(created_at__gte=first_day_of_month).count()
            
            stats_data = {
                'total_reviews_written': total_reviews,
                'average_rating_given': round(avg_rating_given, 2),
                'verified_reviews_count': verified_count,
                'total_helpful_votes_received': total_helpful_votes,
                'most_helpful_review': most_helpful_data,
                'reviews_this_month': reviews_this_month
            }
        
        serializer = UserReviewStatsSerializer(stats_data)
        return Response(serializer.data)
