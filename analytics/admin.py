from django.contrib import admin
from .models import PerformanceAnalytics, TopicPerformance, Suggestion

@admin.register(PerformanceAnalytics)
class PerformanceAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['student', 'total_tests_taken', 'average_score', 'highest_score', 'lowest_score']
    list_filter = ('last_updated',)
    search_fields = ['student__username']

@admin.register(TopicPerformance)
class TopicPerformanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'topic', 'correct_attempts', 'total_attempts', 'percentage_correct']
    list_filter = ('topic',)
    search_fields = ['student__username', 'topic']

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['student', 'category', 'topic', 'created_at', 'action_taken']
    list_filter = ('category', 'created_at')
    search_fields = ['student__username', 'topic']
