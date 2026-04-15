from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    subject = models.CharField(max_length=100, null=True, blank=True)
    duration_minutes = models.IntegerField(default=30)
    total_questions = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.created_by.username}"
    
    class Meta:
        ordering = ['-created_at']


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    topic = models.CharField(max_length=100, null=True, blank=True)
    marks = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}: {self.text[:50]}"
    
    class Meta:
        ordering = ['quiz', 'order']


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.question.text[:50]} - {self.text[:50]}"
    
    class Meta:
        ordering = ['question', 'order']


class Result(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    time_taken_seconds = models.IntegerField(default=0)
    attempted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} ({self.percentage}%)"
    
    class Meta:
        ordering = ['-attempted_at']
        unique_together = ('student', 'quiz')


class StudentAnswer(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.result.student.username} - {self.question.text[:50]}"
    
    class Meta:
        ordering = ['question__order']
