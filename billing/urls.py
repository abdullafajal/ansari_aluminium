"""
URL configuration for billing app.
"""
from django.urls import path
from . import views

app_name = "billing"

urlpatterns = [
    path("", views.invoice_list, name="list"),
    path("invoice/<int:pk>/", views.invoice_detail, name="detail"),
    path("invoice/<int:pk>/pdf/", views.invoice_pdf, name="pdf"),
    path("invoice/<int:pk>/download/", views.invoice_pdf_download, name="pdf_download"),
    path("invoice/<int:pk>/add-payment/", views.add_payment, name="add_payment"),
    path("payments/", views.payment_list, name="payments"),
    # Public share link (no login required)
    path("share/<uuid:share_id>/", views.invoice_public_pdf, name="public_pdf"),
]
