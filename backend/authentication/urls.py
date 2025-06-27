"""
URL configuration for authentication app.
"""
from django.urls import path
from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    logout_view,
    verify_token_view
)

app_name = 'authentication'

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', logout_view, name='logout'),
    path('verify/', verify_token_view, name='verify-token'),
]
