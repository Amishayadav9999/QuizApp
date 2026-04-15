from django.db import models
from accounts.models import User
from quizzes.models import Quiz, Result

class PerformanceAnalytics(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='performance_analytics')
    total_tests_taken = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    highest_score = models.FloatField(default=0.0)
    lowest_score = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics for {self.student.username}"
    
    class Meta:
        verbose_name_plural = "Performance Analytics"


class TopicPerformance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='topic_performance')
    topic = models.CharField(max_length=100)
    correct_attempts = models.IntegerField(default=0)
    total_attempts = models.IntegerField(default=0)
    percentage_correct = models.FloatField(default=0.0)
    last_attempted = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.topic}: {self.percentage_correct}%"
    
    class Meta:
        unique_together = ('student', 'topic')
        ordering = ['percentage_correct']


class Suggestion(models.Model):
    CATEGORY_CHOICES = (
        ('weak', 'Weak Topic'),
        ('improvement', 'Improvement Area'),
        ('strength', 'Strength'),
        ('resource', 'Learning Resource'),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='suggestions')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    topic = models.CharField(max_length=100)
    suggestion_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    action_taken = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student.username} - {self.topic} ({self.category})"
    
    class Meta:
        ordering = ['-created_at']
