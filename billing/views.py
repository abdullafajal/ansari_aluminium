"""
Billing and invoice views.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string

from core.utils import render_to_pdf
from .models import Invoice, Payment


@login_required
def invoice_list(request):
    """List invoices."""
    user = request.user
    
    if user.is_admin:
        invoices = Invoice.objects.select_related("order__quotation__customer").all()
    else:
        customer = getattr(user, "customer_profile", None)
        if customer:
            invoices = Invoice.objects.filter(order__quotation__customer=customer)
        else:
            invoices = Invoice.objects.none()
    
    # Filter by status
    status = request.GET.get("status")
    if status:
        invoices = invoices.filter(status=status)
    
    return render(request, "billing/list.html", {
        "invoices": invoices,
        "status_choices": Invoice.Status.choices,
        "current_status": status,
    })


@login_required
def invoice_detail(request, pk):
    """View invoice details."""
    invoice = get_object_or_404(Invoice, pk=pk)
    
    # Permission check
    if not request.user.is_admin:
        customer = getattr(request.user, "customer_profile", None)
        if not customer or invoice.order.quotation.customer != customer:
            messages.error(request, "You don't have permission to view this invoice.")
            return redirect("billing:list")
    
    payments = invoice.payments.all()
    
    return render(request, "billing/detail.html", {
        "invoice": invoice,
        "order": invoice.order,
        "payments": payments,
        "payment_methods": Payment.Method.choices,
    })


@login_required
def invoice_pdf(request, pk):
    """View invoice PDF preview (HTML)."""
    invoice = get_object_or_404(Invoice, pk=pk)
    
    from dynamic_preferences.registries import global_preferences_registry
    global_preferences = global_preferences_registry.manager()
    
    html = render_to_string("billing/pdf_template.html", {
        "invoice": invoice,
        "order": invoice.order,
        "items": invoice.order.quotation.items.all(),
        "is_public": False,
        "global_preferences": global_preferences,
    })
    
    return HttpResponse(html, content_type="text/html")


@login_required
def invoice_pdf_download(request, pk):
    """Download invoice PDF."""
    invoice = get_object_or_404(Invoice, pk=pk)
    
    from dynamic_preferences.registries import global_preferences_registry
    global_preferences = global_preferences_registry.manager()
    
    return render_to_pdf(
        "billing/pdf_template.html",
        {
            "invoice": invoice,
            "order": invoice.order,
            "items": invoice.order.quotation.items.all(),
            "is_public": False,
            "global_preferences": global_preferences,
        },
        request=request,
        filename=f"{invoice.invoice_number}.pdf"
    )





def invoice_public_pdf(request, share_id):
    """Public PDF download for invoice (Direct Download)."""
    invoice = get_object_or_404(Invoice, share_id=share_id)
    
    from dynamic_preferences.registries import global_preferences_registry
    global_preferences = global_preferences_registry.manager()
    
    return render_to_pdf(
        "billing/pdf_template.html",
        {
            "invoice": invoice,
            "order": invoice.order,
            "items": invoice.order.quotation.items.all(),
            "is_public": True,
            "global_preferences": global_preferences,
        },
        request=request,
        filename=f"{invoice.invoice_number}.pdf"
    )


@login_required
def add_payment(request, pk):
    """Add payment to invoice."""
    if not request.user.is_admin:
        messages.error(request, "Only admins can record payments.")
        return redirect("billing:list")
    
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if request.method == "POST":
        amount = float(request.POST.get("amount", 0))
        method = request.POST.get("method", Payment.Method.CASH)
        reference = request.POST.get("reference", "")
        notes = request.POST.get("notes", "")
        
        if amount > 0:
            invoice.add_payment(
                amount=amount,
                method=method,
                reference=reference,
                notes=notes,
                user=request.user
            )
            messages.success(request, f"Payment of ₹{amount:,.2f} recorded!")
        else:
            messages.error(request, "Please enter a valid amount.")
    
    return redirect("billing:detail", pk=invoice.pk)


@login_required
def payment_list(request):
    """List all payments (admin only)."""
    if not request.user.is_admin:
        messages.error(request, "Only admins can view all payments.")
        return redirect("billing:list")
    
    payments = Payment.objects.select_related("invoice__order__quotation__customer").all()
    
    return render(request, "billing/payments.html", {
        "payments": payments,
    })



