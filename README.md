# SmartQuiz - Intelligent Quiz Platform

## 🚀 Project Overview

SmartQuiz is a comprehensive Django-based quiz management system with **AI-powered analytics and personalized learning suggestions**. It features role-based authentication, quiz creation tools for teachers, and an interactive quiz-taking experience for students with instant performance analysis.

## 📋 Key Features

### 1. **Multi-Role Authentication System**
- **Admin**: Full system management from Django admin panel
- **Teacher**: Create quizzes, manage questions/answers, view student results
- **Student**: Take quizzes, view results, receive AI suggestions

### 2. **Quiz System**
- Create unlimited quizzes with multiple-choice questions
- Support for multiple correct answers per question
- Customizable duration and marking scheme
- Publish/unpublish quizzes for control

### 3. **Smart Result Analysis**
- Automatic score calculation
- Percentage-based grading
- Student answer tracking
- Correct vs. incorrect answer comparison

### 4. **AI-Powered Analytics** 🎯
- **Performance Analytics**: Track average scores, highest/lowest scores
- **Topic-wise Performance**: Identify weak and strong subjects
- **Personalized Suggestions**: Get actionable learning recommendations
- **Categories of Suggestions**:
  - ⚠️ Weak Topic: "You are weak in Python loops. Practice more..."
  - 📈 Improvement Area: "You can improve in..."
  - ⭐ Your Strength: "Great job! You are strong in..."
  - 📚 Learning Resource: "Consider reviewing tutorials..."

### 5. **Dashboards**
- **Admin Dashboard**: Monitor total students, teachers, quizzes
- **Teacher Dashboard**: View created quizzes, student attempts, analytics
- **Student Dashboard**: Track attempted quizzes, scores, AI suggestions, weak topics

### 6. **Additional Features**
- 🏆 Student Leaderboard with rankings
- ⏱️ Quiz Timer with auto-submission
- 📊 Beautiful Bootstrap UI with responsive design
- 🎨 Modern gradient design with smooth animations

## 📁 Project Structure

```
SmartQuiz/
├── smartquiz_config/       # Main Django configuration
│   ├── settings.py         # Settings with custom user model
│   ├── urls.py            # Main URL routing
│   └── wsgi.py
│
├── accounts/              # Authentication & User Management
│   ├── models.py          # Custom User model with roles
│   ├── views.py           # Register, Login, Profile
│   ├── forms.py           # Registration & Login forms
│   ├── urls.py
│   └── admin.py           # Admin interface
│
├── teachers/              # Teacher Dashboard & Quiz Management
│   ├── models.py          # TeacherProfile model
│   ├── views.py           # Dashboard, Quiz CRUD operations
│   ├── urls.py
│   └── admin.py
│
├── students/              # Student Quiz Attempt & Results
│   ├── models.py          # StudentProfile model
│   ├── views.py           # Dashboard, Quiz taking, Results
│   ├── urls.py
│   └── admin.py
│
├── quizzes/               # Core Quiz System
│   ├── models.py          # Quiz, Question, Answer, Result models
│   ├── views.py           # Quiz display views
│   ├── forms.py           # Quiz forms
│   ├── urls.py
│   └── admin.py
│
├── analytics/             # AI Analytics & Suggestions
│   ├── models.py          # Performance, Topic, Suggestion models
│   ├── views.py           # Analytics dashboards
│   ├── utils.py           # AI analysis functions
│   ├── urls.py
│   └── admin.py
│
├── templates/             # HTML templates with Bootstrap
│   ├── base.html         # Base template with navigation
│   ├── home.html         # Landing page
│   ├── accounts/         # Auth templates
│   ├── teachers/         # Teacher templates
│   ├── students/         # Student templates
│   ├── analytics/        # Analytics templates
│   └── quizzes/          # Quiz templates
│
├── static/               # CSS and JavaScript
│   ├── css/
│   └── js/
│
├── db.sqlite3            # SQLite database
├── manage.py             # Django management script
├── venv/                 # Python virtual environment
└── requirements.txt      # Project dependencies
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Steps

1. **Navigate to SmartQuiz directory**:
   ```bash
   cd d:\practice\neww\SmartQuiz
   ```

2. **Activate virtual environment**:
   ```bash
   venv\Scripts\activate
   ```

3. **Run migrations** (already done):
   ```bash
   python manage.py migrate
   ```

4. **Create superuser** (already done):
   - Username: `admin`
   - Password: `admin123`

5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   - Home: `http://localhost:8000/`
   - Admin: `http://localhost:8000/admin/`

## 👥 Test Accounts

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: Administrator
- **Access**: Django admin panel at `/admin/`

### Optional Test Accounts (Create via Register)
You can create test accounts for:
- **Teacher**: Register with teacher role to create quizzes
- **Student**: Register with student role to take quizzes

## 📝 Usage Guide

### For Teachers

1. **Register/Login** with Teacher role
2. **Create Quiz**:
   - Go to Teacher Dashboard → Create New Quiz
   - Add quiz details (title, description, subject, duration)
   - Click "Create Quiz"

3. **Add Questions**:
   - In Quiz edit page, click "Add Question"
   - Enter question text, topic, marks, order
   - Add multiple answers with "Add Answer" button

4. **Mark Correct Answers**:
   - When adding answers, check "is_correct" for right answers
   - Each question can have multiple correct answers

5. **Publish Quiz**:
   - Click "Publish" button to make quiz available to students
   - Click "Unpublish" to hide it again

6. **View Results**:
   - Click "Results" on any quiz to see student attempts
   - View detailed performance of each student

### For Students

1. **Register/Login** with Student role
2. **Browse Quizzes**:
   - Go to "Quizzes" section
   - View all published quizzes by teachers

3. **Take Quiz**:
   - Click "Start Quiz" on any quiz
   - Timer will start automatically
   - Select answer for each question using radio buttons
   - Click "Submit Quiz" when done

4. **View Results**:
   - See score, percentage, and instant feedback
   - View detailed answer review with correct answers
   - Receive AI-powered suggestions

5. **Track Progress**:
   - Check "My Results" for result history
   - View "Dashboard" for analytics
   - See weak/strong topics and improvement suggestions
   - Check leaderboard ranking

### For Admin

1. **Login** with admin credentials
2. **Access Django Admin** at `/admin/`
3. **Manage**:
   - Users (create, edit, delete, assign roles)
   - Quizzes (moderate, delete if needed)
   - Results (view analytics)
   - Suggestions (review AI recommendations)

## 🧠 AI Analytics Features

### Performance Analysis
The system automatically analyzes each student's performance:

```python
analyze_performance(student) function:
- Calculates total tests taken
- Computes average, highest, lowest scores
- Updates performance analytics in database
- Calls topic performance updater
```

### Topic Performance Tracking
```python
update_topic_performance(student) function:
- Identifies all topics attempted by student
- Calculates correct/total attempts per topic
- Calculates percentage accuracy
- Stores in TopicPerformance model
```

### Intelligent Suggestions
```python
generate_suggestions(student) function:
- Analyzes weak topics (< 50% accuracy)
- Suggests improvement areas (50-80% accuracy)
- Recognizes strengths (>= 80% accuracy)
- Recommends learning resources
```

### Example Suggestions Generated:
```
"You are weak in Python loops. Your score is 35.0%. 
You got 3 correct out of 10 attempts. Practice more loop-based 
questions and review the fundamentals."

"You can improve in Data Structures. Your current score is 65.0%. 
Focus on difficult questions and practice more advanced concepts."

"Great job! You are strong in Object-Oriented Programming with 85.0% 
accuracy. Keep practicing to maintain and improve further."
```

## 🎨 Modern UI Features

### Bootstrap 5 Integration
- Responsive design for all devices
- Beautiful gradient backgrounds
- Smooth transitions and hover effects
- Interactive alerts and notifications

### Color Scheme
- **Primary**: #6366f1 (Indigo)
- **Secondary**: #8b5cf6 (Purple)
- **Success**: #10b981 (Green)
- **Warning**: #f59e0b (Amber)
- **Danger**: #ef4444 (Red)

## 📊 Database Models

### Accounts
- **User**: Custom user with roles (admin, teacher, student)

### Teachers
- **TeacherProfile**: Additional teacher info (department, specialization)

### Students
- **StudentProfile**: Student details (roll number, class, section)

### Quizzes
- **Quiz**: Quiz metadata and settings
- **Question**: Individual questions with marks and topic
- **Answer**: Answer options with correctness flag
- **Result**: Student quiz attempt results
- **StudentAnswer**: Tracking of student's selected answers

### Analytics
- **PerformanceAnalytics**: Overall performance metrics
- **TopicPerformance**: Topic-wise accuracy tracking
- **Suggestion**: AI-generated personalized suggestions

## 🔒 Security Features

- Custom user model with role-based access control
- Login required decorators on protected views
- CSRF protection on all forms
- Secure password hashing
- Email field validation
- File upload security (profile pictures)

## 🚀 Deployment Notes

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS` with your domain
3. Use environment variables for sensitive data
4. Set up a production database (PostgreSQL recommended)
5. Use gunicorn/uwsgi as application server
6. Configure reverse proxy (nginx/apache)
7. Set up SSL/TLS certificates

## 📦 Dependencies

- Django 5.2.13
- Pillow (for image handling)
- Bootstrap 5 (via CDN)
- Chart.js (via CDN)

## 🐛 Troubleshooting

### Server won't start
```bash
# Check for syntax errors
python manage.py check

# Verify database is set up
python manage.py migrate

# Clear cache if needed
python manage.py clear_cache
```

### Static files not loading
```bash
# Collect static files
python manage.py collectstatic
```

### "No such table" error
```bash
# Run migrations
python manage.py migrate
```

## 📞 Support & Maintenance

The application includes:
- Django admin interface for data management
- Automatic model validation
- Proper error handling and user feedback
- Responsive error pages

## 🎓 Learning Path

### For New Users:
1. Register as a Student
2. Take a quiz
3. View your results and AI suggestions
4. Create another account as Teacher
5. Create sample quizzes with questions
6. Have students attempt your quizzes
7. Review analytics and student performance

### For Developers:
1. Review the models in each app
2. Understand the view logic
3. Examine the template structure
4. Study the analytics utility functions
5. Extend with additional features

## ✨ Future Enhancements

Potential features to add:
- PDF result export
- Email notifications
- Quiz scheduling
- Peer-to-peer tutoring
- Video explanations
- API endpoints (REST/GraphQL)
- Mobile app
- Real-time notifications
- Quiz categories/tags
- Quiz difficulty levels
- Question shuffling
- Answer randomization
- Timed submissions
- Bulk upload questions (CSV/Excel)

## 📄 License

This project is open-source and available for educational purposes.

---

**Happy Learning! 🎉**

For questions or issues, review the code comments or consult Django documentation.
