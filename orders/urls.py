"""
URL configuration for orders app.
"""
from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.order_list, name="list"),
    path("<int:pk>/", views.order_detail, name="detail"),
    path("<int:pk>/update-status/", views.order_update_status, name="update_status"),
    path("technicians/", views.technician_list, name="technicians"),
    # Public tracking
    path("track/", views.track_order, name="track"),
]
