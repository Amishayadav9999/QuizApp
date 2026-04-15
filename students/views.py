from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Avg, Count
from django.utils import timezone
import time

from quizzes.models import Quiz, Result, StudentAnswer, Question, Answer
from quizzes.forms import QuizAttemptForm
from analytics.utils import analyze_performance, generate_suggestions, get_student_dashboard_stats
from analytics.models import Suggestion, TopicPerformance

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'student':
            return view_func(request, *args, **kwargs)
        return redirect('accounts:login')
    return wrapper

@login_required(login_url='accounts:login')
@student_required
def student_dashboard(request):
    stats = get_student_dashboard_stats(request.user)
    
    context = {
        'stats': stats,
    }
    return render(request, 'students/dashboard.html', context)

@login_required(login_url='accounts:login')
@student_required
def available_quizzes(request):
    """List all published quizzes available for the student"""
    quizzes = Quiz.objects.filter(is_published=True).select_related('created_by')
    
    # Check which quizzes student has already attempted
    attempted_quizzes = Result.objects.filter(student=request.user).values_list('quiz_id')
    
    context = {
        'quizzes': quizzes,
        'attempted_quizzes': [q[0] for q in attempted_quizzes],
    }
    return render(request, 'students/quizzes.html', context)

@login_required(login_url='accounts:login')
@student_required
@require_http_methods(["GET"])
def take_quiz(request, quiz_id):
    """Display quiz questions for student to attempt"""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    
    # Check if student has already attempted this quiz
    existing_result = Result.objects.filter(student=request.user, quiz=quiz).first()
    if existing_result:
        messages.warning(request, 'You have already attempted this quiz!')
        return redirect('students:result_detail', result_id=existing_result.id)
    
    questions = quiz.questions.all().prefetch_related('answers')
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'duration_minutes': quiz.duration_minutes,
    }
    return render(request, 'students/take_quiz.html', context)

@login_required(login_url='accounts:login')
@student_required
@require_http_methods(["POST"])
def submit_quiz(request, quiz_id):
    """Process quiz submission and calculate score"""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    student = request.user
    
    # Check if already attempted
    if Result.objects.filter(student=student, quiz=quiz).exists():
        messages.error(request, 'You have already attempted this quiz!')
        return redirect('students:quizzes')
    
    questions = quiz.questions.all()
    score = 0
    total_marks = 0
    start_time = request.POST.get('start_time')
    
    # Create result object
    result = Result.objects.create(
        student=student,
        quiz=quiz,
        time_taken_seconds=0
    )
    
    # Process each question
    for question in questions:
        total_marks += question.marks
        selected_answer_id = request.POST.get(f'answer_{question.id}')
        
        if selected_answer_id:
            try:
                selected_answer = Answer.objects.get(id=selected_answer_id)
                is_correct = selected_answer.is_correct
                
                if is_correct:
                    score += question.marks
                
                # Record student answer
                StudentAnswer.objects.create(
                    result=result,
                    question=question,
                    selected_answer=selected_answer,
                    is_correct=is_correct
                )
            except Answer.DoesNotExist:
                # Answer not found, mark as incorrect
                StudentAnswer.objects.create(
                    result=result,
                    question=question,
                    is_correct=False
                )
        else:
            # No answer selected
            StudentAnswer.objects.create(
                result=result,
                question=question,
                is_correct=False
            )
    
    # Update result
    result.score = score
    result.total_marks = total_marks
    result.percentage = (score / total_marks * 100) if total_marks > 0 else 0
    result.save()
    
    # Analyze performance and generate suggestions
    analyze_performance(student)
    generate_suggestions(student)
    
    messages.success(request, f'Quiz submitted! Your score: {score}/{total_marks} ({result.percentage:.1f}%)')
    return redirect('students:result_detail', result_id=result.id)

@login_required(login_url='accounts:login')
@student_required
def my_results(request):
    """Show all quiz results for the student"""
    results = Result.objects.filter(student=request.user).order_by('-attempted_at')
    
    context = {
        'results': results,
    }
    return render(request, 'students/results.html', context)

@login_required(login_url='accounts:login')
def result_detail(request, result_id):
    """Show detailed result with AI suggestions"""
    result = get_object_or_404(Result, id=result_id)
    
    # Allow access if user is the student or the teacher who created the quiz
    if request.user.role == 'student':
        if result.student != request.user:
            return redirect('accounts:login')
    elif request.user.role == 'teacher':
        if result.quiz.created_by != request.user:
            return redirect('accounts:login')
    else:
        return redirect('accounts:login')
    
    student_answers = result.answers.all().select_related('question', 'selected_answer')
    suggestions = Suggestion.objects.filter(student=result.student)
    weak_topics = TopicPerformance.objects.filter(student=result.student, percentage_correct__lt=50)
    
    context = {
        'result': result,
        'student_answers': student_answers,
        'suggestions': suggestions,
        'weak_topics': weak_topics,
    }
    return render(request, 'students/result_detail.html', context)

@login_required(login_url='accounts:login')
@student_required
def leaderboard(request):
    """Show leaderboard of students based on average scores"""
    # Get average scores for all students
    results = Result.objects.values('student__id', 'student__username', 'student__first_name', 'student__last_name').annotate(
        avg_percentage=Avg('percentage'),
        total_attempts=Count('id')
    ).order_by('-avg_percentage')[:100]
    
    # Get current student's rank
    student_avg = Result.objects.filter(student=request.user).aggregate(Avg('percentage'))['percentage__avg'] or 0
    student_rank = Result.objects.values('student').annotate(
        avg=Avg('percentage')
    ).filter(avg__gt=student_avg).count() + 1
    
    context = {
        'leaderboard': results,
        'student_rank': student_rank,
        'student_avg': student_avg,
    }
    return render(request, 'students/leaderboard.html', context)
