from django.db.models import Avg, Count, Q, Max, Min
from quizzes.models import Result, StudentAnswer, Quiz
from analytics.models import PerformanceAnalytics, TopicPerformance, Suggestion
from accounts.models import User

def analyze_performance(student):
    """
    Analyze student performance and update analytics
    - Calculate average score
    - Find weak topics
    - Generate suggestions
    """
    results = Result.objects.filter(student=student)
    
    if not results.exists():
        return None
    
    # Calculate overall stats
    total_tests = results.count()
    average_score = results.aggregate(Avg('percentage'))['percentage__avg'] or 0
    highest_score = results.aggregate(max_score=Max('percentage'))['max_score'] or 0
    lowest_score = results.aggregate(min_score=Min('percentage'))['min_score'] or 0
    
    # Create or update analytics
    analytics, created = PerformanceAnalytics.objects.get_or_create(student=student)
    analytics.total_tests_taken = total_tests
    analytics.average_score = round(average_score, 2)
    analytics.highest_score = highest_score
    analytics.lowest_score = lowest_score
    analytics.save()
    
    # Update topic performance
    update_topic_performance(student)
    
    return analytics


def update_topic_performance(student):
    """
    Update performance metrics for each topic
    """
    results = Result.objects.filter(student=student)
    topics = set()
    
    # Collect all topics
    for result in results:
        student_answers = result.answers.all()
        for answer in student_answers:
            if answer.question.topic:
                topics.add(answer.question.topic)
    
    # Update topic performance for each topic
    for topic in topics:
        student_answers = StudentAnswer.objects.filter(
            result__student=student,
            question__topic=topic
        )
        
        total_attempts = student_answers.count()
        correct_attempts = student_answers.filter(is_correct=True).count()
        percentage = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0
        
        topic_perf, created = TopicPerformance.objects.get_or_create(
            student=student,
            topic=topic
        )
        topic_perf.correct_attempts = correct_attempts
        topic_perf.total_attempts = total_attempts
        topic_perf.percentage_correct = round(percentage, 2)
        topic_perf.save()


def generate_suggestions(student):
    """
    Generate AI-like suggestions based on performance
    """
    # Delete old suggestions and create new ones
    Suggestion.objects.filter(student=student).delete()
    
    topic_performance = TopicPerformance.objects.filter(student=student).order_by('percentage_correct')
    
    suggestions_created = []
    
    # Generate weak topic suggestions
    for topic_perf in topic_performance[:3]:  # Bottom 3 topics
        if topic_perf.percentage_correct < 50:
            suggestion_text = f"You are weak in {topic_perf.topic}. Your score is {topic_perf.percentage_correct:.1f}%. " \
                            f"You got {topic_perf.correct_attempts} correct out of {topic_perf.total_attempts} attempts. " \
                            f"Practice more {topic_perf.topic}-based questions and review the fundamentals."
            
            suggestion = Suggestion.objects.create(
                student=student,
                category='weak',
                topic=topic_perf.topic,
                suggestion_text=suggestion_text
            )
            suggestions_created.append(suggestion)
    
    # Generate improvement suggestions
    for topic_perf in topic_performance[3:6]:  # Middle topics
        if 50 <= topic_perf.percentage_correct < 80:
            suggestion_text = f"You can improve in {topic_perf.topic}. Your current score is {topic_perf.percentage_correct:.1f}%. " \
                            f"Focus on difficult questions and practice more advanced concepts."
            
            suggestion = Suggestion.objects.create(
                student=student,
                category='improvement',
                topic=topic_perf.topic,
                suggestion_text=suggestion_text
            )
            suggestions_created.append(suggestion)
    
    # Generate strength recognition
    strong_topics = topic_performance.filter(percentage_correct__gte=80)[:3]
    for topic_perf in strong_topics:
        suggestion_text = f"Great job! You are strong in {topic_perf.topic} with {topic_perf.percentage_correct:.1f}% accuracy. " \
                        f"Keep practicing to maintain and improve further."
        
        suggestion = Suggestion.objects.create(
            student=student,
            category='strength',
            topic=topic_perf.topic,
            suggestion_text=suggestion_text
        )
        suggestions_created.append(suggestion)
    
    # Generate learning resource suggestions
    weakest_topics = TopicPerformance.objects.filter(student=student).order_by('percentage_correct')[:2]
    for topic_perf in weakest_topics:
        if topic_perf.percentage_correct < 60:
            suggestion_text = f"Resource Suggestion: Consider reviewing online tutorials, textbooks, or educational videos for {topic_perf.topic}. " \
                            f"Join study groups and discuss with peers. Practice problems regularly."
            
            suggestion = Suggestion.objects.create(
                student=student,
                category='resource',
                topic=topic_perf.topic,
                suggestion_text=suggestion_text
            )
            suggestions_created.append(suggestion)
    
    return suggestions_created


def get_student_dashboard_stats(student):
    """
    Get all stats needed for student dashboard
    """
    results = Result.objects.filter(student=student)
    analytics = PerformanceAnalytics.objects.filter(student=student).first()
    recent_results = results[:5]
    suggestions = Suggestion.objects.filter(student=student)
    
    return {
        'total_tests': results.count(),
        'average_score': analytics.average_score if analytics else 0,
        'highest_score': analytics.highest_score if analytics else 0,
        'recent_results': recent_results,
        'weak_topics': TopicPerformance.objects.filter(student=student, percentage_correct__lt=50).order_by('percentage_correct'),
        'strong_topics': TopicPerformance.objects.filter(student=student, percentage_correct__gte=80).order_by('-percentage_correct'),
        'suggestions': suggestions,
    }


def get_admin_dashboard_stats():
    """
    Get stats for admin dashboard
    """
    from teachers.models import TeacherProfile
    from students.models import StudentProfile
    
    total_students = StudentProfile.objects.count()
    total_teachers = TeacherProfile.objects.count()
    total_quizzes = Quiz.objects.count()
    total_results = Result.objects.count()
    
    return {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_quizzes': total_quizzes,
        'total_results': total_results,
    }


def get_teacher_dashboard_stats(teacher):
    """
    Get stats for teacher dashboard
    """
    from quizzes.models import Quiz
    
    quizzes = Quiz.objects.filter(created_by=teacher)
    total_quizzes = quizzes.count()
    total_students_attempted = Result.objects.filter(quiz__in=quizzes).values('student').distinct().count()
    average_quiz_score = Result.objects.filter(quiz__in=quizzes).aggregate(Avg('percentage'))['percentage__avg'] or 0
    
    return {
        'total_quizzes': total_quizzes,
        'total_students_attempted': total_students_attempted,
        'average_quiz_score': round(average_quiz_score, 2),
        'quizzes': quizzes,
    }
