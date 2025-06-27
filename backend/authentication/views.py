"""
Authentication views for JWT token management.
"""
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from users.serializers import UserLoginSerializer, UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token obtain view with user login tracking.
    """
    serializer_class = UserLoginSerializer
    
    @extend_schema(
        summary="User login",
        description="Authenticate user and return JWT tokens"
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Update login tracking
            from django.utils import timezone
            user.last_login = timezone.now()
            user.login_count += 1
            user.save(update_fields=['last_login', 'login_count'])
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Login successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom JWT token refresh view.
    """
    
    @extend_schema(
        summary="Refresh JWT token",
        description="Get a new access token using refresh token"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(
    summary="User logout",
    description="Logout user and blacklist refresh token"
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Logout view that blacklists the refresh token.
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error': 'Invalid token'
        }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Verify JWT token",
    description="Verify if the JWT token is valid"
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_token_view(request):
    """
    Verify if the provided token is valid.
    """
    return Response({
        'message': 'Token is valid',
        'user': UserSerializer(request.user).data
    }, status=status.HTTP_200_OK)
