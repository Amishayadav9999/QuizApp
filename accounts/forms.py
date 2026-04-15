from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import User
from teachers.models import TeacherProfile
from students.models import StudentProfile

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
            if user.role == 'teacher':
                TeacherProfile.objects.create(user=user)
            elif user.role == 'student':
                StudentProfile.objects.create(user=user)
        return user


class CustomUserChangeForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
