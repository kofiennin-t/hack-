"""
URL configuration for ai_models app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AIModelViewSet

app_name = 'ai_models'

router = DefaultRouter()
router.register(r'', AIModelViewSet, basename='aimodel')

urlpatterns = [
    path('', include(router.urls)),
]
