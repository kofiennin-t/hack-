"""
User views for API endpoints.
"""
from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count, Avg
from drf_spectacular.utils import extend_schema
from core.permissions import IsOwnerOrAdmin, IsUserOrAdmin
from .models import User
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
    UserListSerializer,
    PasswordChangeSerializer
)


class UserViewSet(ModelViewSet):
    """
    ViewSet for managing users.
    """
    queryset = User.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated, IsUserOrAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'email', 'created_at', 'last_login']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action == 'list':
            return UserListSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Regular users can only see themselves and other basic user info
        if not self.request.user.is_staff:
            if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
                queryset = queryset.filter(id=self.request.user.id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by email verification
        verified = self.request.query_params.get('verified')
        if verified is not None:
            verified_bool = verified.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(email_verified=verified_bool)
        
        return queryset
    
    @extend_schema(
        summary="Change user password",
        description="Change the current user's password"
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request, pk=None):
        """Change user password."""
        user = self.get_object()
        
        # Ensure user can only change their own password
        if user != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only change your own password'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Update session auth hash to prevent logout
            update_session_auth_hash(request, user)
            
            return Response({'message': 'Password changed successfully'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Get user statistics",
        description="Get statistics about the user's activity"
    )
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get user statistics."""
        user = self.get_object()
        
        # Ensure user can only see their own stats
        if user != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only view your own statistics'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Import here to avoid circular imports
        from user_history.models import UserHistory
        from reviews.models import ModelReview
        
        stats = {
            'total_interactions': UserHistory.objects.filter(user=user).count(),
            'total_reviews': ModelReview.objects.filter(user=user).count(),
            'average_rating_given': ModelReview.objects.filter(user=user).aggregate(
                avg_rating=Avg('rating')
            )['avg_rating'] or 0,
            'unique_models_used': UserHistory.objects.filter(user=user).values('model').distinct().count(),
            'account_age_days': (user.created_at.date() - user.date_joined.date()).days if hasattr(user, 'date_joined') else 0,
        }
        
        return Response(stats)
    
    @extend_schema(
        summary="Deactivate user account",
        description="Deactivate the user's account"
    )
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate user account."""
        user = self.get_object()
        
        # Ensure user can only deactivate their own account or admin
        if user != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only deactivate your own account'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user.status = 'inactive'
        user.is_active = False
        user.save()
        
        return Response({'message': 'Account deactivated successfully'})


class UserRegistrationView(generics.CreateAPIView):
    """
    View for user registration.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        summary="Register a new user",
        description="Create a new user account"
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message': 'User registered successfully',
                    'user': UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(generics.RetrieveUpdateAPIView):
    """
    View for current user profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer
