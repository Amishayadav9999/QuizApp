from django.db import models
from accounts.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    class_name = models.CharField(max_length=100, null=True, blank=True)
    section = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Student: {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']
