"""
Model Review models for the platform.
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import BaseModel
from users.models import User


class ModelReview(BaseModel):
    """
    User reviews for AI models.
    """
    # Core relationships
    model = models.ForeignKey('ai_models.AIModel', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    
    # Review content
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1-5 stars"
    )
    review_title = models.CharField(max_length=200)
    review_text = models.TextField()
    
    # Verification and moderation
    is_verified_user = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    
    # Community engagement
    helpful_votes = models.PositiveIntegerField(default=0)
    total_votes = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'model_reviews'
        verbose_name = 'Model Review'
        verbose_name_plural = 'Model Reviews'
        unique_together = ['model', 'user']  # One review per user per model
        indexes = [
            models.Index(fields=['model']),
            models.Index(fields=['user']),
            models.Index(fields=['rating']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_approved']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.model.name} ({self.rating}★)"
    
    def save(self, *args, **kwargs):
        # Set verification status based on user's interaction history
        if not self.pk:  # Only on creation
            from user_history.models import UserHistory
            user_interactions = UserHistory.objects.filter(
                user=self.user,
                model=self.model,
                response_status='success'
            ).count()
            
            # User is verified if they have at least 3 successful interactions with the model
            self.is_verified_user = user_interactions >= 3
        
        super().save(*args, **kwargs)
        
        # Update model's average rating
        self.model.update_rating()
    
    def delete(self, *args, **kwargs):
        model = self.model
        super().delete(*args, **kwargs)
        # Update model's average rating after deletion
        model.update_rating()
    
    @property
    def helpfulness_ratio(self):
        """Calculate helpfulness ratio."""
        if self.total_votes == 0:
            return 0
        return (self.helpful_votes / self.total_votes) * 100
    
    def vote_helpful(self, is_helpful=True):
        """Add a vote for helpfulness."""
        if is_helpful:
            self.helpful_votes += 1
        self.total_votes += 1
        self.save(update_fields=['helpful_votes', 'total_votes'])


class ReviewVote(BaseModel):
    """
    Track user votes on reviews for helpfulness.
    """
    VOTE_CHOICES = [
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
    ]
    
    review = models.ForeignKey(ModelReview, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_votes')
    vote_type = models.CharField(max_length=20, choices=VOTE_CHOICES)
    
    class Meta:
        db_table = 'review_votes'
        verbose_name = 'Review Vote'
        verbose_name_plural = 'Review Votes'
        unique_together = ['review', 'user']  # One vote per user per review
        indexes = [
            models.Index(fields=['review']),
            models.Index(fields=['user']),
            models.Index(fields=['vote_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.review.review_title} ({self.vote_type})"
    
    def save(self, *args, **kwargs):
        is_new = not self.pk
        was_helpful = None
        
        if not is_new:
            # Get old vote before saving
            old_vote = ReviewVote.objects.get(pk=self.pk)
            was_helpful = old_vote.vote_type == 'helpful'
        
        super().save(*args, **kwargs)
        
        # Update review vote counts
        if is_new:
            # New vote
            if self.vote_type == 'helpful':
                self.review.helpful_votes += 1
            self.review.total_votes += 1
        else:
            # Changed vote
            if was_helpful and self.vote_type == 'not_helpful':
                self.review.helpful_votes -= 1
            elif not was_helpful and self.vote_type == 'helpful':
                self.review.helpful_votes += 1
        
        self.review.save(update_fields=['helpful_votes', 'total_votes'])
    
    def delete(self, *args, **kwargs):
        review = self.review
        was_helpful = self.vote_type == 'helpful'
        
        super().delete(*args, **kwargs)
        
        # Update review vote counts
        if was_helpful:
            review.helpful_votes -= 1
        review.total_votes -= 1
        review.save(update_fields=['helpful_votes', 'total_votes'])
