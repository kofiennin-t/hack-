"""
User History views for API endpoints.
"""
from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count, Avg, Sum, Min, Max, Q
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema
from core.permissions import IsUserOrAdmin
from .models import UserHistory
from .serializers import (
    UserHistorySerializer,
    UserHistoryListSerializer,
    UserHistoryCreateSerializer,
    UserHistoryUpdateSerializer,
    UserHistoryStatsSerializer,
    SessionStatsSerializer
)


class UserHistoryViewSet(ModelViewSet):
    """
    ViewSet for managing user history.
    """
    queryset = UserHistory.objects.select_related('user', 'model', 'model__developer').all()
    permission_classes = [permissions.IsAuthenticated, IsUserOrAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['prompt', 'response', 'session_id']
    ordering_fields = ['created_at', 'response_time_ms', 'user_rating', 'cost_incurred']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UserHistoryListSerializer
        elif self.action == 'create':
            return UserHistoryCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserHistoryUpdateSerializer
        return UserHistorySerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Regular users can only see their own history
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        
        # Filter by model
        model_id = self.request.query_params.get('model')
        if model_id:
            queryset = queryset.filter(model_id=model_id)
        
        # Filter by session
        session_id = self.request.query_params.get('session')
        if session_id:
            queryset = queryset.filter(session_id=session_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(response_status=status_filter)
        
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
        
        return queryset
    
    @extend_schema(
        summary="Get user's interaction statistics",
        description="Get comprehensive statistics about the user's interactions with AI models"
    )
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get user interaction statistics."""
        user_history = self.get_queryset()
        
        if not user_history.exists():
            return Response({
                'total_interactions': 0,
                'unique_models': 0,
                'unique_sessions': 0,
                'average_rating': 0,
                'total_cost': 0,
                'average_response_time': 0,
                'success_rate': 0,
                'total_tokens': 0,
                'most_used_model': None,
                'interactions_today': 0,
                'interactions_this_month': 0
            })
        
        # Basic statistics
        stats = user_history.aggregate(
            total_interactions=Count('id'),
            unique_models=Count('model', distinct=True),
            unique_sessions=Count('session_id', distinct=True),
            average_rating=Avg('user_rating'),
            total_cost=Sum('cost_incurred'),
            average_response_time=Avg('response_time_ms'),
            total_tokens=Sum('input_tokens') + Sum('output_tokens')
        )
        
        # Success rate
        successful_interactions = user_history.filter(response_status='success').count()
        total_interactions = stats['total_interactions']
        stats['success_rate'] = (successful_interactions / total_interactions * 100) if total_interactions > 0 else 0
        
        # Most used model
        most_used = user_history.values('model__name').annotate(
            count=Count('id')
        ).order_by('-count').first()
        stats['most_used_model'] = most_used['model__name'] if most_used else None
        
        # Time-based statistics
        today = timezone.now().date()
        stats['interactions_today'] = user_history.filter(created_at__date=today).count()
        
        first_day_of_month = today.replace(day=1)
        stats['interactions_this_month'] = user_history.filter(
            created_at__date__gte=first_day_of_month
        ).count()
        
        # Round decimal values
        if stats['average_rating']:
            stats['average_rating'] = round(stats['average_rating'], 2)
        if stats['total_cost']:
            stats['total_cost'] = round(float(stats['total_cost']), 6)
        if stats['average_response_time']:
            stats['average_response_time'] = round(stats['average_response_time'], 2)
        if stats['success_rate']:
            stats['success_rate'] = round(stats['success_rate'], 2)
        
        # Handle None values
        for key, value in stats.items():
            if value is None:
                stats[key] = 0
        
        serializer = UserHistoryStatsSerializer(stats)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Get user's sessions",
        description="Get all unique sessions for the user with statistics"
    )
    @action(detail=False, methods=['get'])
    def sessions(self, request):
        """Get user's unique sessions."""
        sessions = self.get_queryset().values('session_id').annotate(
            interaction_count=Count('id'),
            first_interaction=Min('created_at'),
            last_interaction=Max('created_at'),
            unique_models=Count('model', distinct=True),
            total_cost=Sum('cost_incurred'),
            average_response_time=Avg('response_time_ms')
        ).order_by('-last_interaction')
        
        # Round decimal values
        for session in sessions:
            if session['total_cost']:
                session['total_cost'] = round(float(session['total_cost']), 6)
            if session['average_response_time']:
                session['average_response_time'] = round(session['average_response_time'], 2)
        
        serializer = SessionStatsSerializer(sessions, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Get interaction timeline",
        description="Get user's interaction timeline with daily aggregations"
    )
    @action(detail=False, methods=['get'])
    def timeline(self, request):
        """Get user interaction timeline."""
        # Get date range from query params
        days = int(request.query_params.get('days', 30))
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        # Get daily aggregations
        daily_stats = self.get_queryset().filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        ).extra(
            select={'day': 'date(created_at)'}
        ).values('day').annotate(
            interactions=Count('id'),
            successful_interactions=Count('id', filter=Q(response_status='success')),
            total_cost=Sum('cost_incurred'),
            average_response_time=Avg('response_time_ms'),
            unique_models=Count('model', distinct=True)
        ).order_by('day')
        
        # Calculate success rate and round values
        for day_stat in daily_stats:
            total = day_stat['interactions']
            successful = day_stat['successful_interactions']
            day_stat['success_rate'] = (successful / total * 100) if total > 0 else 0
            
            if day_stat['total_cost']:
                day_stat['total_cost'] = round(float(day_stat['total_cost']), 6)
            if day_stat['average_response_time']:
                day_stat['average_response_time'] = round(day_stat['average_response_time'], 2)
            if day_stat['success_rate']:
                day_stat['success_rate'] = round(day_stat['success_rate'], 2)
        
        return Response(daily_stats)
    
    @extend_schema(
        summary="Export user history",
        description="Export user's interaction history in CSV format"
    )
    @action(detail=False, methods=['get'])
    def export(self, request):
        """Export user history to CSV."""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_history.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Date', 'Model', 'Session ID', 'Prompt', 'Response Status',
            'Response Time (ms)', 'Input Tokens', 'Output Tokens',
            'Cost', 'Rating', 'Feedback'
        ])
        
        for history in self.get_queryset():
            writer.writerow([
                history.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                history.model.name,
                history.session_id,
                history.prompt[:100] + '...' if len(history.prompt) > 100 else history.prompt,
                history.get_response_status_display(),
                history.response_time_ms,
                history.input_tokens,
                history.output_tokens,
                float(history.cost_incurred),
                history.user_rating or '',
                history.user_feedback[:100] + '...' if history.user_feedback and len(history.user_feedback) > 100 else history.user_feedback or ''
            ])
        
        return response
