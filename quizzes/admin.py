from django.contrib import admin
from .models import Quiz, Question, Answer, Result, StudentAnswer

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'is_published', 'created_at']
    list_filter = ('is_published', 'created_at')
    search_fields = ['title']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'topic', 'marks', 'order']
    list_filter = ('quiz', 'topic')
    search_fields = ['text']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct']
    list_filter = ('is_correct',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'score', 'percentage', 'attempted_at']
    list_filter = ('quiz', 'attempted_at')
    search_fields = ['student__username']

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['result', 'question', 'is_correct']
    list_filter = ('is_correct',)
