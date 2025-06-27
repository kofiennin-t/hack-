"""
API Logs views for API endpoints.
"""
from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count, Avg, Sum, Q, Min, Max
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema
from core.permissions import IsOwnerOrAdmin
from .models import APIUsageLog, APIMetrics
from .serializers import (
    APIUsageLogSerializer,
    APIUsageLogListSerializer,
    APIUsageLogCreateSerializer,
    APIMetricsSerializer,
    APIStatsSerializer,
    DeveloperAPIStatsSerializer,
    ModelAPIStatsSerializer
)


class APIUsageLogViewSet(ModelViewSet):
    """
    ViewSet for managing API usage logs.
    """
    queryset = APIUsageLog.objects.select_related('user', 'developer', 'model').all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['request_path', 'ip_address', 'user_agent', 'error_message']
    ordering_fields = ['created_at', 'processing_time_ms', 'response_status_code']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return APIUsageLogListSerializer
        elif self.action == 'create':
            return APIUsageLogCreateSerializer
        return APIUsageLogSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Regular users can only see their own logs
        if not self.request.user.is_staff:
            if hasattr(self.request.user, 'developer_profile'):
                # Developers can see logs for their models
                queryset = queryset.filter(
                    Q(user=self.request.user) | 
                    Q(developer=self.request.user.developer_profile)
                )
            else:
                # Regular users can only see their own logs
                queryset = queryset.filter(user=self.request.user)
        
        # Filter by model
        model_id = self.request.query_params.get('model')
        if model_id:
            queryset = queryset.filter(model_id=model_id)
        
        # Filter by developer
        developer_id = self.request.query_params.get('developer')
        if developer_id:
            queryset = queryset.filter(developer_id=developer_id)
        
        # Filter by status code
        status_code = self.request.query_params.get('status_code')
        if status_code:
            try:
                queryset = queryset.filter(response_status_code=int(status_code))
            except ValueError:
                pass
        
        # Filter by success/failure
        success_filter = self.request.query_params.get('success')
        if success_filter is not None:
            if success_filter.lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(response_status_code__range=(200, 299))
            else:
                queryset = queryset.exclude(response_status_code__range=(200, 299))
        
        # Filter by date range
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if date_from:
            try:
                from datetime import datetime
                date_from_obj = datetime.fromisoformat(date_from.replace('Z', '+00:00'))
                queryset = queryset.filter(created_at__gte=date_from_obj)
            except ValueError:
                pass
        
        if date_to:
            try:
                from datetime import datetime
                date_to_obj = datetime.fromisoformat(date_to.replace('Z', '+00:00'))
                queryset = queryset.filter(created_at__lte=date_to_obj)
            except ValueError:
                pass
        
        # Filter by request method
        method = self.request.query_params.get('method')
        if method:
            queryset = queryset.filter(request_method=method.upper())
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Create API usage log entry."""
        # This endpoint is typically used by the system itself
        # to log API usage, not by end users
        return super().create(request, *args, **kwargs)


class APIMetricsViewSet(ModelViewSet):
    """
    ViewSet for API metrics (read-only for users).
    """
    queryset = APIMetrics.objects.select_related('model', 'developer').all()
    serializer_class = APIMetricsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['period_start', 'total_requests', 'success_rate']
    ordering = ['-period_start']
    http_method_names = ['get', 'head', 'options']  # Read-only
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Non-admin users can only see metrics for their own resources
        if not self.request.user.is_staff:
            if hasattr(self.request.user, 'developer_profile'):
                queryset = queryset.filter(developer=self.request.user.developer_profile)
            else:
                # Regular users cannot see metrics
                queryset = queryset.none()
        
        # Filter by period type
        period_type = self.request.query_params.get('period_type')
        if period_type:
            queryset = queryset.filter(period_type=period_type)
        
        # Filter by model
        model_id = self.request.query_params.get('model')
        if model_id:
            queryset = queryset.filter(model_id=model_id)
        
        # Filter by developer
        developer_id = self.request.query_params.get('developer')
        if developer_id:
            queryset = queryset.filter(developer_id=developer_id)
        
        return queryset


@extend_schema(
    summary="Get general API statistics",
    description="Get platform-wide API usage statistics"
)
@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def api_stats_view(request):
    """Get general API statistics (Admin only)."""
    # Time range
    days = int(request.query_params.get('days', 30))
    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)
    
    logs = APIUsageLog.objects.filter(created_at__gte=start_date)
    
    # Basic stats
    total_requests = logs.count()
    successful_requests = logs.filter(response_status_code__range=(200, 299)).count()
    failed_requests = total_requests - successful_requests
    
    success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 0
    error_rate = (failed_requests / total_requests * 100) if total_requests > 0 else 0
    
    # Performance stats
    avg_response_time = logs.aggregate(avg_time=Avg('processing_time_ms'))['avg_time'] or 0
    total_data = logs.aggregate(
        total_data=Sum('request_size_bytes') + Sum('response_size_bytes')
    )['total_data'] or 0
    
    # Unique counts
    unique_users = logs.values('user').distinct().count()
    unique_models = logs.values('model').distinct().count()
    
    # Time-based stats
    today = timezone.now().date()
    requests_today = logs.filter(created_at__date=today).count()
    
    first_day_of_month = today.replace(day=1)
    requests_this_month = logs.filter(created_at__date__gte=first_day_of_month).count()
    
    # Top models
    top_models = logs.values('model__name').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Error distribution
    error_dist = logs.exclude(
        response_status_code__range=(200, 299)
    ).values('response_status_code').annotate(
        count=Count('id')
    ).order_by('-count')
    
    error_distribution = {
        str(item['response_status_code']): item['count']
        for item in error_dist
    }
    
    stats_data = {
        'total_requests': total_requests,
        'successful_requests': successful_requests,
        'failed_requests': failed_requests,
        'success_rate': round(success_rate, 2),
        'error_rate': round(error_rate, 2),
        'average_response_time': round(avg_response_time, 2),
        'total_data_transferred': total_data,
        'unique_users': unique_users,
        'unique_models': unique_models,
        'requests_today': requests_today,
        'requests_this_month': requests_this_month,
        'top_models': list(top_models),
        'error_distribution': error_distribution
    }
    
    serializer = APIStatsSerializer(stats_data)
    return Response(serializer.data)


@extend_schema(
    summary="Get developer API statistics",
    description="Get API usage statistics for a specific developer"
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def developer_api_stats_view(request, developer_id):
    """Get API statistics for a specific developer."""
    from developers.models import Developer
    
    try:
        developer = Developer.objects.get(id=developer_id)
    except Developer.DoesNotExist:
        return Response(
            {'error': 'Developer not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Permission check
    if (not request.user.is_staff and 
        not (hasattr(request.user, 'developer_profile') and 
             request.user.developer_profile == developer)):
        return Response(
            {'error': 'Permission denied'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Time range
    days = int(request.query_params.get('days', 30))
    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)
    
    logs = APIUsageLog.objects.filter(
        developer=developer,
        created_at__gte=start_date
    )
    
    # Basic stats
    total_requests = logs.count()
    successful_requests = logs.filter(response_status_code__range=(200, 299)).count()
    failed_requests = total_requests - successful_requests
    
    success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 0
    avg_response_time = logs.aggregate(avg_time=Avg('processing_time_ms'))['avg_time'] or 0
    total_data = logs.aggregate(
        total_data=Sum('request_size_bytes') + Sum('response_size_bytes')
    )['total_data'] or 0
    
    unique_users = logs.values('user').distinct().count()
    
    # Time-based stats
    today = timezone.now().date()
    requests_today = logs.filter(created_at__date=today).count()
    
    first_day_of_month = today.replace(day=1)
    requests_this_month = logs.filter(created_at__date__gte=first_day_of_month).count()
    
    # Top performing models
    top_models = logs.values('model__name').annotate(
        count=Count('id'),
        avg_time=Avg('processing_time_ms')
    ).order_by('-count')[:5]
    
    # Recent errors
    recent_errors = logs.exclude(
        response_status_code__range=(200, 299)
    ).order_by('-created_at')[:5].values(
        'model__name', 'response_status_code', 'error_message', 'created_at'
    )
    
    stats_data = {
        'total_requests': total_requests,
        'successful_requests': successful_requests,
        'failed_requests': failed_requests,
        'success_rate': round(success_rate, 2),
        'average_response_time': round(avg_response_time, 2),
        'total_data_transferred': total_data,
        'unique_users': unique_users,
        'requests_today': requests_today,
        'requests_this_month': requests_this_month,
        'top_performing_models': list(top_models),
        'recent_errors': list(recent_errors)
    }
    
    serializer = DeveloperAPIStatsSerializer(stats_data)
    return Response(serializer.data)


@extend_schema(
    summary="Get model API statistics",
    description="Get API usage statistics for a specific model"
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def model_api_stats_view(request, model_id):
    """Get API statistics for a specific model."""
    from ai_models.models import AIModel
    
    try:
        model = AIModel.objects.get(id=model_id)
    except AIModel.DoesNotExist:
        return Response(
            {'error': 'Model not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Time range
    days = int(request.query_params.get('days', 30))
    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)
    
    logs = APIUsageLog.objects.filter(
        model=model,
        created_at__gte=start_date
    )
    
    # Basic stats
    total_requests = logs.count()
    successful_requests = logs.filter(response_status_code__range=(200, 299)).count()
    failed_requests = total_requests - successful_requests
    
    success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 0
    avg_response_time = logs.aggregate(avg_time=Avg('processing_time_ms'))['avg_time'] or 0
    total_data = logs.aggregate(
        total_data=Sum('request_size_bytes') + Sum('response_size_bytes')
    )['total_data'] or 0
    
    unique_users = logs.values('user').distinct().count()
    
    # Time-based stats
    today = timezone.now().date()
    requests_today = logs.filter(created_at__date=today).count()
    
    first_day_of_month = today.replace(day=1)
    requests_this_month = logs.filter(created_at__date__gte=first_day_of_month).count()
    
    # Hourly distribution (last 24 hours)
    last_24h = timezone.now() - timedelta(hours=24)
    hourly_logs = logs.filter(created_at__gte=last_24h)
    
    hourly_distribution = {}
    for i in range(24):
        hour_start = last_24h + timedelta(hours=i)
        hour_end = hour_start + timedelta(hours=1)
        hour_count = hourly_logs.filter(
            created_at__gte=hour_start,
            created_at__lt=hour_end
        ).count()
        hourly_distribution[hour_start.strftime('%H:00')] = hour_count
    
    # Status code distribution
    status_dist = logs.values('response_status_code').annotate(
        count=Count('id')
    ).order_by('response_status_code')
    
    status_code_distribution = {
        str(item['response_status_code']): item['count']
        for item in status_dist
    }
    
    # Recent performance trend (daily averages)
    daily_trend = []
    for i in range(7):  # Last 7 days
        day_start = (timezone.now() - timedelta(days=i)).replace(hour=0, minute=0, second=0)
        day_end = day_start + timedelta(days=1)
        
        day_logs = logs.filter(created_at__gte=day_start, created_at__lt=day_end)
        avg_time = day_logs.aggregate(avg_time=Avg('processing_time_ms'))['avg_time'] or 0
        
        daily_trend.append({
            'date': day_start.strftime('%Y-%m-%d'),
            'average_response_time': round(avg_time, 2),
            'request_count': day_logs.count()
        })
    
    stats_data = {
        'total_requests': total_requests,
        'successful_requests': successful_requests,
        'failed_requests': failed_requests,
        'success_rate': round(success_rate, 2),
        'average_response_time': round(avg_response_time, 2),
        'total_data_transferred': total_data,
        'unique_users': unique_users,
        'requests_today': requests_today,
        'requests_this_month': requests_this_month,
        'hourly_distribution': hourly_distribution,
        'status_code_distribution': status_code_distribution,
        'recent_performance_trend': daily_trend
    }
    
    serializer = ModelAPIStatsSerializer(stats_data)
    return Response(serializer.data)
