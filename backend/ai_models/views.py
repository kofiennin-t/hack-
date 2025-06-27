"""
AI Model views for API endpoints.
"""
from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count, Avg, Sum, Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from core.permissions import IsOwnerDeveloperOrAdmin, IsDeveloperOrAdmin
from .models import AIModel
from .serializers import (
    AIModelSerializer,
    AIModelCreateSerializer,
    AIModelUpdateSerializer,
    AIModelListSerializer,
    AIModelStatsSerializer,
    AIModelSearchSerializer
)


class AIModelFilter:
    """
    Custom filter class for AI models.
    """
    @staticmethod
    def filter_queryset(queryset, request):
        # Filter by category
        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by pricing type
        pricing_type = request.query_params.get('pricing_type')
        if pricing_type:
            queryset = queryset.filter(pricing_type=pricing_type)
        
        # Filter by developer
        developer_id = request.query_params.get('developer')
        if developer_id:
            queryset = queryset.filter(developer_id=developer_id)
        
        # Filter by minimum rating
        min_rating = request.query_params.get('min_rating')
        if min_rating:
            try:
                min_rating_float = float(min_rating)
                queryset = queryset.filter(average_rating__gte=min_rating_float)
            except ValueError:
                pass
        
        # Filter by tags
        tags = request.query_params.get('tags')
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            for tag in tag_list:
                queryset = queryset.filter(tags__icontains=tag)
        
        # Filter by supported languages
        language = request.query_params.get('language')
        if language:
            queryset = queryset.filter(supported_languages__icontains=language)
        
        # Price range filtering
        max_price = request.query_params.get('max_price')
        if max_price:
            try:
                max_price_float = float(max_price)
                queryset = queryset.filter(
                    Q(price_per_request__lte=max_price_float) |
                    Q(price_per_token__lte=max_price_float)
                )
            except ValueError:
                pass
        
        return queryset


class AIModelViewSet(ModelViewSet):
    """
    ViewSet for managing AI models.
    """
    queryset = AIModel.objects.select_related('developer__user').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'tags', 'category']
    ordering_fields = [
        'name', 'created_at', 'average_rating', 'total_requests',
        'price_per_request', 'average_response_time'
    ]
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AIModelCreateSerializer
        elif self.action == 'list':
            return AIModelListSerializer
        elif self.action in ['update', 'partial_update']:
            return AIModelUpdateSerializer
        return AIModelSerializer
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, IsDeveloperOrAdmin]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerDeveloperOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # For public listing, only show active and public models
        if self.action == 'list' and not (
            self.request.user.is_authenticated and 
            hasattr(self.request.user, 'developer_profile')
        ):
            queryset = queryset.filter(status='active', is_public=True)
        
        # Developers can see their own models regardless of status
        elif (self.request.user.is_authenticated and 
              hasattr(self.request.user, 'developer_profile') and
              not self.request.user.is_staff):
            if self.action in ['update', 'partial_update', 'destroy']:
                queryset = queryset.filter(developer=self.request.user.developer_profile)
        
        # Apply custom filters
        queryset = AIModelFilter.filter_queryset(queryset, self.request)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Create AI model."""
        # Check if user has developer profile
        if not hasattr(request.user, 'developer_profile'):
            return Response(
                {'error': 'Only developers can create AI models'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Get AI model statistics",
        description="Get comprehensive statistics for the AI model"
    )
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get AI model statistics."""
        model = self.get_object()
        
        # Import here to avoid circular imports
        from user_history.models import UserHistory
        from reviews.models import ModelReview
        from django.utils import timezone
        from datetime import timedelta
        
        # Calculate statistics
        interactions = UserHistory.objects.filter(model=model)
        total_interactions = interactions.count()
        unique_users = interactions.values('user').distinct().count()
        
        # Calculate revenue
        total_revenue = 0
        if model.pricing_type == 'per_request':
            total_revenue = float(model.price_per_request) * model.total_requests
        elif model.pricing_type == 'per_token':
            total_tokens = interactions.aggregate(
                total=Sum('input_tokens') + Sum('output_tokens')
            )['total'] or 0
            total_revenue = float(model.price_per_token) * total_tokens
        
        # Time-based metrics
        today = timezone.now().date()
        requests_today = interactions.filter(created_at__date=today).count()
        
        first_day_of_month = today.replace(day=1)
        requests_this_month = interactions.filter(created_at__date__gte=first_day_of_month).count()
        
        stats_data = {
            'total_requests': model.total_requests,
            'total_interactions': total_interactions,
            'unique_users': unique_users,
            'average_response_time': round(model.average_response_time, 2),
            'success_rate': round(model.success_rate, 2),
            'average_rating': round(model.average_rating, 2),
            'total_reviews': model.total_reviews,
            'total_revenue': round(total_revenue, 2),
            'requests_today': requests_today,
            'requests_this_month': requests_this_month,
        }
        
        serializer = AIModelStatsSerializer(stats_data)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Get model reviews",
        description="Get all reviews for the AI model"
    )
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get model reviews."""
        model = self.get_object()
        
        # Import here to avoid circular imports
        from reviews.models import ModelReview
        from reviews.serializers import ModelReviewSerializer
        
        reviews = ModelReview.objects.filter(model=model).order_by('-created_at')
        serializer = ModelReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Get model usage history",
        description="Get usage history for the AI model"
    )
    @action(detail=True, methods=['get'], permission_classes=[IsOwnerDeveloperOrAdmin])
    def usage_history(self, request, pk=None):
        """Get model usage history."""
        model = self.get_object()
        
        # Import here to avoid circular imports
        from user_history.models import UserHistory
        from user_history.serializers import UserHistoryListSerializer
        
        history = UserHistory.objects.filter(model=model).order_by('-created_at')
        
        # Pagination
        from core.pagination import CustomPageNumberPagination
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(history, request)
        
        if page is not None:
            serializer = UserHistoryListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = UserHistoryListSerializer(history, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Search AI models",
        description="Advanced search for AI models"
    )
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced search for AI models."""
        queryset = self.get_queryset()
        
        # Search query
        query = request.query_params.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__icontains=query) |
                Q(category__icontains=query) |
                Q(developer__developer_name__icontains=query)
            )
        
        # Apply ordering
        ordering = request.query_params.get('ordering', '-average_rating')
        if ordering in ['rating', '-rating']:
            ordering = ordering.replace('rating', 'average_rating')
        elif ordering in ['requests', '-requests']:
            ordering = ordering.replace('requests', 'total_requests')
        
        queryset = queryset.order_by(ordering)
        
        # Pagination
        from core.pagination import CustomPageNumberPagination
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        
        if page is not None:
            serializer = AIModelSearchSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = AIModelSearchSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Get featured models",
        description="Get featured AI models"
    )
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured AI models."""
        # Featured models are those with high ratings and good performance
        queryset = self.get_queryset().filter(
            status='active',
            is_public=True,
            average_rating__gte=4.0,
            total_requests__gte=100
        ).order_by('-average_rating', '-total_requests')[:12]
        
        serializer = AIModelListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Get model categories",
        description="Get list of available model categories"
    )
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get available model categories."""
        categories = [
            {'value': choice[0], 'label': choice[1]}
            for choice in AIModel.MODEL_CATEGORY_CHOICES
        ]
        return Response(categories)
