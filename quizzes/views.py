from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from quizzes.models import Quiz, Question

def all_quizzes(request):
    """List all published quizzes"""
    quizzes = Quiz.objects.filter(is_published=True).select_related('created_by')
    
    context = {
        'quizzes': quizzes,
    }
    return render(request, 'quizzes/all_quizzes.html', context)

def quiz_detail(request, pk):
    """Show detailed information about a quiz"""
    quiz = get_object_or_404(Quiz, id=pk, is_published=True)
    questions = quiz.questions.all()
    
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'quizzes/detail.html', context)
