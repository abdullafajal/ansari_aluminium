"""
URL configuration for dashboard app.
"""
from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("enquiries/", views.enquiry_list, name="enquiry_list"),
    path("enquiries/<int:pk>/", views.enquiry_detail, name="enquiry_detail"),
]
