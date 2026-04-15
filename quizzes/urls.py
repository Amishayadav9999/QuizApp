from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('all/', views.all_quizzes, name='all_quizzes'),
    path('<int:pk>/', views.quiz_detail, name='detail'),
]
