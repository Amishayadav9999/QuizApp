from django.contrib import admin
from .models import TeacherProfile

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'specialization', 'experience_years', 'created_at']
    list_filter = ('department',)
    search_fields = ['user__username', 'user__first_name']
