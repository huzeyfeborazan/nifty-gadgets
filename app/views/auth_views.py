"""Authentication related views."""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def register_view(request):
    """This is the register page view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('app:dashboard')
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
    form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})

def login_view(request):
    """This is the login page view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('app:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'app/login.html')

def logout_view(request):
    """This is the logout page view"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('app:home')
