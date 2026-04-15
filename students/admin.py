from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'roll_number', 'class_name', 'section', 'created_at']
    list_filter = ('class_name', 'section')
    search_fields = ['user__username', 'user__first_name', 'roll_number']
