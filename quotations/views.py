"""
Quotation management views.
"""
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta

from core.utils import AdminRequiredMixin, render_to_pdf
from customers.models import Customer
from .models import Quotation, QuotationItem
from orders.models import Order


@login_required
def quotation_list(request):
    """List quotations."""
    user = request.user
    
    if user.is_admin:
        quotations = Quotation.objects.select_related("customer").all()
    else:
        # Customer sees only their quotations
        customer = getattr(user, "customer_profile", None)
        if customer:
            quotations = Quotation.objects.filter(customer=customer)
        else:
            quotations = Quotation.objects.none()
    
    # Filter by status
    status = request.GET.get("status")
    if status:
        quotations = quotations.filter(status=status)
    
    return render(request, "quotations/list.html", {
        "quotations": quotations,
        "status_choices": Quotation.Status.choices,
        "current_status": status,
    })


@login_required
def quotation_create(request):
    """Create new quotation."""
    if not request.user.is_admin:
        messages.error(request, "Only admins can create quotations.")
        return redirect("quotations:list")
    
    customers = Customer.objects.filter(is_active=True)
    
    # Build customer data for JavaScript auto-fill
    customer_data = {
        str(c.pk): {
            'address': c.full_address,
            'company': c.company_name or c.contact_person,
        }
        for c in customers
    }
    
    if request.method == "POST":
        customer_id = request.POST.get("customer")
        customer = get_object_or_404(Customer, pk=customer_id)
        
        valid_days = int(request.POST.get("valid_days", 15))
        discount_percent = Decimal(request.POST.get("discount_percent", 0) or 0)
        gst_percent = Decimal(request.POST.get("gst_percent", 18) or 18)
        material_cost = Decimal(request.POST.get("material_cost", 0) or 0)
        labour_cost = Decimal(request.POST.get("labour_cost", 0) or 0)
        
        quotation = Quotation.objects.create(
            customer=customer,
            valid_until=timezone.now().date() + timedelta(days=valid_days),
            created_by=request.user,
            discount_percent=discount_percent,
            gst_percent=gst_percent,
            material_cost=material_cost,
            labour_cost=labour_cost,
            site_address=request.POST.get("site_address", ""),
            terms=request.POST.get("terms", ""),
        )
        
        # Add items
        descriptions = request.POST.getlist("item_description")
        quantities = request.POST.getlist("item_quantity")
        rates = request.POST.getlist("item_rate")
        widths = request.POST.getlist("item_width")
        heights = request.POST.getlist("item_height")
        
        for i, desc in enumerate(descriptions):
            if desc.strip():
                QuotationItem.objects.create(
                    quotation=quotation,
                    description=desc,
                    quantity=float(quantities[i]) if quantities[i] else 1,
                    rate=float(rates[i]) if rates[i] else 0,
                    width=float(widths[i]) if widths[i] else None,
                    height=float(heights[i]) if heights[i] else None,
                    order=i,
                )
        
        quotation.calculate_totals()
        messages.success(request, f"Quotation {quotation.quote_number} created!")
        return redirect("quotations:detail", pk=quotation.pk)
    
    import json
    return render(request, "quotations/create.html", {
        "customers": customers,
        "customer_data_json": json.dumps(customer_data),
    })


@login_required
def quotation_detail(request, pk):
    """View quotation details."""
    quotation = get_object_or_404(Quotation, pk=pk)
    
    # Permission check
    if not request.user.is_admin:
        customer = getattr(request.user, "customer_profile", None)
        if not customer or quotation.customer != customer:
            messages.error(request, "You don't have permission to view this quotation.")
            return redirect("quotations:list")
    
    # Get next allowed statuses for step-by-step transitions
    next_statuses = quotation.get_next_statuses()
    
    return render(request, "quotations/detail.html", {
        "quotation": quotation,
        "items": quotation.items.all(),
        "next_statuses": next_statuses,
    })


@login_required
def quotation_edit(request, pk):
    """Edit quotation."""
    if not request.user.is_admin:
        messages.error(request, "Only admins can edit quotations.")
        return redirect("quotations:list")
    
    quotation = get_object_or_404(Quotation, pk=pk)
    
    if request.method == "POST":
        quotation.discount_percent = Decimal(request.POST.get("discount_percent") or "0")
        quotation.gst_percent = Decimal(request.POST.get("gst_percent") or "18")
        quotation.material_cost = Decimal(request.POST.get("material_cost") or "0")
        quotation.labour_cost = Decimal(request.POST.get("labour_cost") or "0")
        quotation.notes = request.POST.get("notes", "")
        quotation.terms = request.POST.get("terms", "")
        quotation.save()
        quotation.calculate_totals()
        messages.success(request, "Quotation updated!")
        return redirect("quotations:detail", pk=quotation.pk)
    
    return render(request, "quotations/edit.html", {
        "quotation": quotation,
    })


@login_required
def quotation_pdf(request, pk):
    """Generate PDF for quotation (uses print-friendly HTML)."""
    quotation = get_object_or_404(Quotation, pk=pk)
    
    from dynamic_preferences.registries import global_preferences_registry
    global_preferences = global_preferences_registry.manager()
    
    # Render the template
    html = render_to_string("quotations/pdf_template.html", {
        "quotation": quotation,
        "items": quotation.items.all(),
        "is_public": False,
        "global_preferences": global_preferences,
    })
    
    # Return as print-friendly HTML
    # Users can use browser's Print -> Save as PDF
    return HttpResponse(html, content_type="text/html")





@login_required
def quotation_pdf_download(request, pk):
    """Download PDF for quotation."""
    quotation = get_object_or_404(Quotation, pk=pk)
    
    # Permission check (reuse logic or refactor, copying for now)
    if not request.user.is_admin:
        customer = getattr(request.user, "customer_profile", None)
        if not customer or quotation.customer != customer:
            messages.error(request, "You don't have permission to download this quotation.")
            return redirect("quotations:list")
            
    from dynamic_preferences.registries import global_preferences_registry
    global_preferences = global_preferences_registry.manager()
    
    return render_to_pdf(
        "quotations/pdf_template.html",
        {
            "quotation": quotation,
            "items": quotation.items.all(),
            "is_public": False,
            "global_preferences": global_preferences,
        },
        request=request,
        filename=f"{quotation.quote_number}.pdf"
    )


def quotation_public_pdf(request, share_id):
    """Public PDF download for quotation (Direct Download)."""
    quotation = get_object_or_404(Quotation, share_id=share_id)
    
    from dynamic_preferences.registries import global_preferences_registry
    global_preferences = global_preferences_registry.manager()
                 
    return render_to_pdf(
        "quotations/pdf_template.html",
        {
            "quotation": quotation,
            "items": quotation.items.all(),
            "is_public": True,
            "global_preferences": global_preferences,
        },
        request=request,
        filename=f"{quotation.quote_number}.pdf"
    )






@login_required
def quotation_convert(request, pk):
    """Convert quotation to order."""
    if not request.user.is_admin:
        messages.error(request, "Only admins can convert quotations to orders.")
        return redirect("quotations:list")
    
    quotation = get_object_or_404(Quotation, pk=pk)
    
    if hasattr(quotation, "order"):
        messages.warning(request, "This quotation already has an order.")
        return redirect("orders:detail", pk=quotation.order.pk)
    
    if request.method == "POST":
        order = Order.objects.create(
            quotation=quotation,
            status=Order.Status.DRAFT,
            created_by=request.user,
        )
        quotation.status = Quotation.Status.CONVERTED
        quotation.save()
        
        messages.success(request, f"Order {order.order_number} created from quotation!")
        return redirect("orders:detail", pk=order.pk)
    
    return render(request, "quotations/convert.html", {
        "quotation": quotation,
    })


@login_required
def quotation_send(request, pk):
    """Mark quotation as sent."""
    if not request.user.is_admin:
        messages.error(request, "Only admins can send quotations.")
        return redirect("quotations:list")
    
    quotation = get_object_or_404(Quotation, pk=pk)
    quotation.status = Quotation.Status.SENT
    quotation.save()
    
    messages.success(request, f"Quotation {quotation.quote_number} marked as sent!")
    return redirect("quotations:detail", pk=quotation.pk)


@login_required
def quotation_update_status(request, pk):
    """Update quotation status (step-by-step only)."""
    if not request.user.is_admin:
        messages.error(request, "Only admins can update quotation status.")
        return redirect("quotations:list")
    
    quotation = get_object_or_404(Quotation, pk=pk)
    
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status and quotation.can_transition_to(new_status):
            quotation.status = new_status
            quotation.save()
            
            # If converted, create an order
            if new_status == Quotation.Status.CONVERTED:
                # Check if order already exists
                if hasattr(quotation, 'order'):
                    messages.info(request, "This quotation already has an order.")
                    return redirect("orders:detail", pk=quotation.order.pk)
                
                # Create new order
                order = Order.objects.create(
                    quotation=quotation,
                    created_by=request.user
                )
                messages.success(request, f"Order {order.order_number} created successfully!")
                return redirect("orders:detail", pk=order.pk)
            
            messages.success(request, f"Quotation status updated to {quotation.get_status_display()}!")
        else:
            messages.error(request, "Invalid status transition. Status can only change step-by-step.")
    
    return redirect("quotations:detail", pk=quotation.pk)

