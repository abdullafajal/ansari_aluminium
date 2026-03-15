"""
Forms for user authentication.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class LoginForm(forms.Form):
    """Login form."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
            "placeholder": "Enter your email"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
            "placeholder": "Enter your password"
        })
    )


class RegisterForm(UserCreationForm):
    """Registration form."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
            "placeholder": "Enter your email"
        })
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
            "placeholder": "First name"
        })
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
            "placeholder": "Last name"
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
            "placeholder": "Create a password"
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
            "placeholder": "Confirm password"
        })
    )
    
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password1", "password2"]
