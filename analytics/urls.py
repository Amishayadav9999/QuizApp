from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.analytics_dashboard, name='dashboard'),
    path('performance/<int:student_id>/', views.student_performance, name='student_performance'),
    path('suggestions/<int:student_id>/', views.student_suggestions, name='student_suggestions'),
]
