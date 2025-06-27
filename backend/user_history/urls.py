"""
URL configuration for user_history app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserHistoryViewSet

app_name = 'user_history'

router = DefaultRouter()
router.register(r'', UserHistoryViewSet, basename='userhistory')

urlpatterns = [
    path('', include(router.urls)),
]
