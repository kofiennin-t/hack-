"""
URL configuration for developers app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeveloperViewSet, DeveloperRegistrationView

app_name = 'developers'

router = DefaultRouter()
router.register(r'', DeveloperViewSet, basename='developer')

urlpatterns = [
    path('register/', DeveloperRegistrationView.as_view(), name='developer-register'),
    path('', include(router.urls)),
]
