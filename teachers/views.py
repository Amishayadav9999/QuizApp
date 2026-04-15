from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Count
from quizzes.models import Quiz, Question, Answer, Result
from quizzes.forms import QuizForm, QuestionForm, AnswerForm
from teachers.models import TeacherProfile

def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'teacher':
            return view_func(request, *args, **kwargs)
        return redirect('accounts:login')
    return wrapper

@login_required(login_url='accounts:login')
@teacher_required
def teacher_dashboard(request):
    teacher = request.user
    quizzes = Quiz.objects.filter(created_by=teacher)
    total_quizzes = quizzes.count()
    total_questions = Question.objects.filter(quiz__in=quizzes).count()
    total_results = Result.objects.filter(quiz__in=quizzes).count()
    published_quizzes = quizzes.filter(is_published=True).count()
    
    context = {
        'total_quizzes': total_quizzes,
        'total_questions': total_questions,
        'total_results': total_results,
        'published_quizzes': published_quizzes,
        'recent_quizzes': quizzes[:5],
    }
    return render(request, 'teachers/dashboard.html', context)

@login_required(login_url='accounts:login')
@teacher_required
def quiz_list(request):
    quizzes = Quiz.objects.filter(created_by=request.user)
    context = {'quizzes': quizzes}
    return render(request, 'teachers/quiz_list.html', context)

@login_required(login_url='accounts:login')
@teacher_required
@require_http_methods(["GET", "POST"])
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            messages.success(request, 'Quiz created successfully!')
            return redirect('teachers:edit_quiz', quiz_id=quiz.id)
    else:
        form = QuizForm()
    
    context = {'form': form}
    return render(request, 'teachers/create_quiz.html', context)

@login_required(login_url='accounts:login')
@teacher_required
@require_http_methods(["GET", "POST"])
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
    
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz updated successfully!')
            return redirect('teachers:quiz_list')
    else:
        form = QuizForm(instance=quiz)
    
    questions = quiz.questions.all()
    context = {
        'form': form,
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'teachers/edit_quiz.html', context)

@login_required(login_url='accounts:login')
@teacher_required
@require_http_methods(["POST"])
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
    quiz.delete()
    messages.success(request, 'Quiz deleted successfully!')
    return redirect('teachers:quiz_list')

@login_required(login_url='accounts:login')
@teacher_required
@require_http_methods(["GET", "POST"])
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'Question added successfully!')
            return redirect('teachers:add_question', quiz_id=quiz.id)
    else:
        form = QuestionForm()
    
    context = {
        'form': form,
        'quiz': quiz,
        'questions': quiz.questions.all(),
    }
    return render(request, 'teachers/add_question.html', context)

@login_required(login_url='accounts:login')
@teacher_required
@require_http_methods(["GET", "POST"])
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id, quiz__created_by=request.user)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question updated successfully!')
            return redirect('teachers:edit_quiz', quiz_id=question.quiz.id)
    else:
        form = QuestionForm(instance=question)
    
    context = {
        'form': form,
        'question': question,
        'answers': question.answers.all(),
    }
    return render(request, 'teachers/edit_question.html', context)

@login_required(login_url='accounts:login')
@teacher_required
@require_http_methods(["POST"])
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id, quiz__created_by=request.user)
    quiz_id = question.quiz.id
    question.delete()
    messages.success(request, 'Question deleted successfully!')
    return redirect('teachers:edit_quiz', quiz_id=quiz_id)

@login_required(login_url='accounts:login')
@teacher_required
@require_http_methods(["GET", "POST"])
def add_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id, quiz__created_by=request.user)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            messages.success(request, 'Answer added successfully!')
            return redirect('teachers:edit_question', question_id=question.id)
    else:
        form = AnswerForm()
    
    context = {
        'form': form,
        'question': question,
        'answers': question.answers.all(),
    }
    return render(request, 'teachers/add_answer.html', context)

@login_required(login_url='accounts:login')
@teacher_required
@require_http_methods(["GET", "POST"])
def edit_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id, question__quiz__created_by=request.user)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Answer updated successfully!')
            return redirect('teachers:edit_question', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    
    context = {
        'form': form,
        'answer': answer,
    }
    return render(request, 'teachers/edit_answer.html', context)

@login_required(login_url='accounts:login')
@teacher_required
@require_http_methods(["POST"])
def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id, question__quiz__created_by=request.user)
    question_id = answer.question.id
    answer.delete()
    messages.success(request, 'Answer deleted successfully!')
    return redirect('teachers:edit_question', question_id=question_id)

@login_required(login_url='accounts:login')
@teacher_required
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
    results = Result.objects.filter(quiz=quiz).order_by('-attempted_at')
    
    context = {
        'quiz': quiz,
        'results': results,
        'total_attempts': results.count(),
    }
    return render(request, 'teachers/quiz_results.html', context)

@login_required(login_url='accounts:login')
@teacher_required
@require_http_methods(["POST"])
def publish_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
    quiz.is_published = not quiz.is_published
    quiz.save()
    
    status = 'published' if quiz.is_published else 'unpublished'
    messages.success(request, f'Quiz {status} successfully!')
    return redirect('teachers:edit_quiz', quiz_id=quiz.id)
