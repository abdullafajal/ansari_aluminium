"""
URL configuration for quotations app.
"""
from django.urls import path
from . import views

app_name = "quotations"

urlpatterns = [
    path("", views.quotation_list, name="list"),
    path("create/", views.quotation_create, name="create"),
    path("<int:pk>/", views.quotation_detail, name="detail"),
    path("<int:pk>/edit/", views.quotation_edit, name="edit"),
    path("<int:pk>/pdf/", views.quotation_pdf, name="pdf"),
    path("<int:pk>/convert/", views.quotation_convert, name="convert"),
    path("<int:pk>/send/", views.quotation_send, name="send"),
    path("<int:pk>/update-status/", views.quotation_update_status, name="update_status"),
    # Public share link (no login required)
    path("share/<uuid:share_id>/", views.quotation_public_pdf, name="public_pdf"),
    path("<int:pk>/download/", views.quotation_pdf_download, name="pdf_download"),
]
