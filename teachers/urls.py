from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='dashboard'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/create/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/edit/', views.edit_quiz, name='edit_quiz'),
    path('quiz/<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),
    path('quiz/<int:quiz_id>/add-question/', views.add_question, name='add_question'),
    path('question/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('question/<int:question_id>/add-answer/', views.add_answer, name='add_answer'),
    path('answer/<int:answer_id>/edit/', views.edit_answer, name='edit_answer'),
    path('answer/<int:answer_id>/delete/', views.delete_answer, name='delete_answer'),
    path('quiz/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
    path('quiz/<int:quiz_id>/publish/', views.publish_quiz, name='publish_quiz'),
]
