from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from accounts.models import User
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm, LoginForm
from teachers.models import TeacherProfile
from students.models import StudentProfile

@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created successfully! Welcome {user.username}')
            login(request, user)
            
            # Redirect based on role
            if user.role == 'teacher':
                return redirect('teachers:dashboard')
            else:
                return redirect('students:dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'teacher':
            return redirect('teachers:dashboard')
        elif request.user.role == 'student':
            return redirect('students:dashboard')
        else:
            return redirect('admin:index')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect based on role
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                
                if user.role == 'teacher':
                    return redirect('teachers:dashboard')
                elif user.role == 'student':
                    return redirect('students:dashboard')
                else:
                    return redirect('admin:index')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required(login_url='accounts:login')
@require_http_methods(["GET"])
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required(login_url='accounts:login')
@require_http_methods(["GET", "POST"])
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})
