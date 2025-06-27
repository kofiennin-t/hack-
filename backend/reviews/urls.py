"""
URL configuration for reviews app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ModelReviewViewSet, ModelReviewStatsView, UserReviewStatsView

app_name = 'reviews'

router = DefaultRouter()
router.register(r'', ModelReviewViewSet, basename='modelreview')

urlpatterns = [
    path('stats/model/<uuid:model_id>/', ModelReviewStatsView.as_view(), name='model-review-stats'),
    path('stats/user/', UserReviewStatsView.as_view(), name='user-review-stats'),
    path('', include(router.urls)),
]
