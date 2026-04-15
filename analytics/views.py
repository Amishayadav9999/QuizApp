from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from analytics.models import PerformanceAnalytics, TopicPerformance, Suggestion
from analytics.utils import get_student_dashboard_stats

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'student':
            return view_func(request, *args, **kwargs)
        return redirect('accounts:login')
    return wrapper

@login_required(login_url='accounts:login')
@student_required
def analytics_dashboard(request):
    """Main analytics dashboard for student"""
    stats = get_student_dashboard_stats(request.user)
    topic_performance = TopicPerformance.objects.filter(student=request.user).order_by('percentage_correct')
    
    context = {
        'stats': stats,
        'topic_performance': topic_performance,
    }
    return render(request, 'analytics/dashboard.html', context)

@login_required(login_url='accounts:login')
@student_required
def student_performance(request, student_id):
    """Detailed performance analytics for a specific student"""
    if student_id != request.user.id and request.user.role != 'admin':
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()
    
    analytics = PerformanceAnalytics.objects.filter(student_id=student_id).first()
    topic_performance = TopicPerformance.objects.filter(student_id=student_id).order_by('percentage_correct')
    
    context = {
        'analytics': analytics,
        'topic_performance': topic_performance,
    }
    return render(request, 'analytics/student_performance.html', context)

@login_required(login_url='accounts:login')
@student_required
def student_suggestions(request, student_id):
    """View suggestions for student"""
    if student_id != request.user.id and request.user.role != 'admin':
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()
    
    suggestions = Suggestion.objects.filter(student_id=student_id).order_by('-created_at')
    weak_suggestions = suggestions.filter(category='weak')
    improvement_suggestions = suggestions.filter(category='improvement')
    strength_suggestions = suggestions.filter(category='strength')
    resource_suggestions = suggestions.filter(category='resource')
    
    context = {
        'suggestions': suggestions,
        'weak_suggestions': weak_suggestions,
        'improvement_suggestions': improvement_suggestions,
        'strength_suggestions': strength_suggestions,
        'resource_suggestions': resource_suggestions,
    }
    return render(request, 'analytics/suggestions.html', context)
