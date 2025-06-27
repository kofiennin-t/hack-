"""
Developer views for API endpoints.
"""
from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count, Avg, Sum
from drf_spectacular.utils import extend_schema
from core.permissions import IsOwnerOrAdmin, IsDeveloperOrAdmin, IsOwnerDeveloperOrAdmin
from .models import Developer
from .serializers import (
    DeveloperSerializer,
    DeveloperRegistrationSerializer,
    DeveloperUpdateSerializer,
    DeveloperListSerializer,
    DeveloperStatsSerializer
)


class DeveloperViewSet(ModelViewSet):
    """
    ViewSet for managing developers.
    """
    queryset = Developer.objects.select_related('user').all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['developer_name', 'company_name', 'specialization']
    ordering_fields = ['developer_name', 'created_at', 'total_revenue', 'is_verified']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DeveloperRegistrationSerializer
        elif self.action == 'list':
            return DeveloperListSerializer
        elif self.action in ['update', 'partial_update']:
            return DeveloperUpdateSerializer
        return DeveloperSerializer
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerDeveloperOrAdmin]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, IsOwnerDeveloperOrAdmin]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by verification status
        verified = self.request.query_params.get('verified')
        if verified is not None:
            verified_bool = verified.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(is_verified=verified_bool)
        
        # Filter by specialization
        specialization = self.request.query_params.get('specialization')
        if specialization:
            queryset = queryset.filter(specialization__icontains=specialization)
        
        # For non-staff users, only show their own profile in certain actions
        if not self.request.user.is_staff and self.action in ['update', 'partial_update', 'destroy']:
            queryset = queryset.filter(user=self.request.user)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Create developer profile."""
        # Check if user already has a developer profile
        if hasattr(request.user, 'developer_profile'):
            return Response(
                {'error': 'User already has a developer profile'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Get developer statistics",
        description="Get comprehensive statistics for the developer"
    )
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get developer statistics."""
        developer = self.get_object()
        
        # Import here to avoid circular imports
        from ai_models.models import AIModel
        from user_history.models import UserHistory
        from reviews.models import ModelReview
        
        # Calculate statistics
        models = AIModel.objects.filter(developer=developer)
        total_models = models.count()
        active_models = models.filter(status='active').count()
        
        # Get interaction count across all developer's models
        total_interactions = UserHistory.objects.filter(
            model__developer=developer
        ).count()
        
        # Get average rating across all models
        avg_rating = ModelReview.objects.filter(
            model__developer=developer
        ).aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        
        stats_data = {
            'total_models': total_models,
            'active_models': active_models,
            'total_interactions': total_interactions,
            'total_revenue': float(developer.total_revenue),
            'avg_model_rating': round(avg_rating, 2),
            'current_month_usage': developer.current_month_usage,
            'quota_limit': developer.monthly_quota_limit,
            'quota_percentage': round(
                (developer.current_month_usage / developer.monthly_quota_limit) * 100, 2
            ) if developer.monthly_quota_limit > 0 else 0
        }
        
        serializer = DeveloperStatsSerializer(stats_data)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Get developer's models",
        description="Get all models created by the developer"
    )
    @action(detail=True, methods=['get'])
    def models(self, request, pk=None):
        """Get developer's models."""
        developer = self.get_object()
        
        # Import here to avoid circular imports
        from ai_models.models import AIModel
        from ai_models.serializers import AIModelListSerializer
        
        models = AIModel.objects.filter(developer=developer).order_by('-created_at')
        
        # Filter by status if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            models = models.filter(status=status_filter)
        
        serializer = AIModelListSerializer(models, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Reset monthly quota usage",
        description="Reset the developer's monthly API usage counter (Admin only)"
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reset_quota(self, request, pk=None):
        """Reset monthly quota usage."""
        developer = self.get_object()
        developer.reset_monthly_usage()
        
        return Response({
            'message': 'Monthly quota usage reset successfully',
            'current_usage': developer.current_month_usage
        })
    
    @extend_schema(
        summary="Verify developer",
        description="Verify developer account (Admin only)"
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def verify(self, request, pk=None):
        """Verify developer account."""
        developer = self.get_object()
        
        from django.utils import timezone
        developer.is_verified = True
        developer.verification_date = timezone.now()
        developer.status = 'active'
        developer.save()
        
        return Response({
            'message': 'Developer verified successfully'
        })


class DeveloperRegistrationView(generics.CreateAPIView):
    """
    View for developer registration.
    """
    queryset = Developer.objects.all()
    serializer_class = DeveloperRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Register as a developer",
        description="Create a developer profile for the current user"
    )
    def create(self, request, *args, **kwargs):
        # Check if user already has a developer profile
        if hasattr(request.user, 'developer_profile'):
            return Response(
                {'error': 'User already has a developer profile'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            developer = serializer.save()
            return Response(
                {
                    'message': 'Developer profile created successfully',
                    'developer': DeveloperSerializer(developer).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
