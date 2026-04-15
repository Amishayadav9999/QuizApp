from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('quizzes/', views.available_quizzes, name='quizzes'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('results/', views.my_results, name='results'),
    path('result/<int:result_id>/', views.result_detail, name='result_detail'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
