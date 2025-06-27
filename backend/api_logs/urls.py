"""
URL configuration for api_logs app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    APIUsageLogViewSet,
    APIMetricsViewSet,
    api_stats_view,
    developer_api_stats_view,
    model_api_stats_view
)

app_name = 'api_logs'

router = DefaultRouter()
router.register(r'usage', APIUsageLogViewSet, basename='apiusagelog')
router.register(r'metrics', APIMetricsViewSet, basename='apimetrics')

urlpatterns = [
    path('stats/', api_stats_view, name='api-stats'),
    path('stats/developer/<uuid:developer_id>/', developer_api_stats_view, name='developer-api-stats'),
    path('stats/model/<uuid:model_id>/', model_api_stats_view, name='model-api-stats'),
    path('', include(router.urls)),
]
