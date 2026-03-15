"""
Views for user authentication.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User
from .forms import LoginForm, RegisterForm


def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect("dashboard:index")
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.email}!")
                next_url = request.GET.get("next", "dashboard:index")
                return redirect(next_url)
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    """User logout view."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("website:home")


def register_view(request):
    """User registration is disabled - admin creates all users."""
    messages.info(request, "Registration is disabled. Please contact the administrator to create an account.")
    return redirect("accounts:login")


@login_required
def profile_view(request):
    """User profile view."""
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")
        user.phone = request.POST.get("phone", "")
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("accounts:profile")
    
    return render(request, "accounts/profile.html")
