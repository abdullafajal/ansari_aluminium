"""
Order management views.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Order, OrderStatusLog, Technician


@login_required
def order_list(request):
    """List orders."""
    user = request.user
    
    if user.is_admin:
        orders = Order.objects.select_related("quotation__customer", "technician").all()
    else:
        customer = getattr(user, "customer_profile", None)
        if customer:
            orders = Order.objects.filter(quotation__customer=customer)
        else:
            orders = Order.objects.none()
    
    # Filter by status
    status = request.GET.get("status")
    if status:
        orders = orders.filter(status=status)
    
    return render(request, "orders/list.html", {
        "orders": orders,
        "status_choices": Order.Status.choices,
        "current_status": status,
    })


@login_required
def order_detail(request, pk):
    """View order details."""
    order = get_object_or_404(Order, pk=pk)
    
    # Permission check
    if not request.user.is_admin:
        customer = getattr(request.user, "customer_profile", None)
        if not customer or order.quotation.customer != customer:
            messages.error(request, "You don't have permission to view this order.")
            return redirect("orders:list")
    
    status_logs = order.status_logs.select_related("changed_by").all()
    next_statuses = order.get_next_statuses()
    
    return render(request, "orders/detail.html", {
        "order": order,
        "quotation": order.quotation,
        "items": order.quotation.items.all(),
        "status_logs": status_logs,
        "next_statuses": next_statuses,
        "technicians": Technician.objects.filter(is_active=True) if request.user.is_admin else [],
    })


@login_required
def order_update_status(request, pk):
    """Update order status (step-by-step only)."""
    if not request.user.is_admin:
        messages.error(request, "Only admins can update order status.")
        return redirect("orders:list")
    
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == "POST":
        new_status = request.POST.get("status")
        notes = request.POST.get("notes", "")
        technician_id = request.POST.get("technician")
        expected_delivery = request.POST.get("expected_delivery")
        
        if new_status and new_status != order.status:
            if order.update_status(new_status, user=request.user, notes=notes):
                messages.success(request, f"Order status updated to {order.get_status_display()}!")
            else:
                messages.error(request, "Invalid status transition. Status can only change step-by-step.")
        
        if technician_id:
            order.technician_id = technician_id
        if expected_delivery:
            order.expected_delivery = expected_delivery
        order.save()
    
    return redirect("orders:detail", pk=order.pk)


@login_required
def technician_list(request):
    """List technicians (admin only)."""
    if not request.user.is_admin:
        messages.error(request, "Only admins can view technicians.")
        return redirect("dashboard:index")
    
    technicians = Technician.objects.all()
    return render(request, "orders/technicians.html", {
        "technicians": technicians,
    })


def track_order(request):
    """Public order tracking view."""
    # Import locally to avoid potential circular imports with top-level
    from quotations.models import Quotation 
    
    query = request.GET.get("q", "").strip()
    order = None
    quotation = None
    error = None
    
    if query:
        # 1. Search by Order Number
        order = Order.objects.filter(order_number__iexact=query).first()
        
        # 2. Search by Quotation Number (if order not found)
        if not order:
            # Check if this quotation has an order
            quotation = Quotation.objects.filter(quote_number__iexact=query).first()
            if quotation and hasattr(quotation, "order"):
                order = quotation.order
    
        # 3. If still no order, but we have a quotation, show quotaion status
        if not order and not quotation:
            quotation = Quotation.objects.filter(quote_number__iexact=query).first()
            
        if not order and not quotation:
            error = f"We couldn't find any order or quotation with number '{query}'. Please check and try again."

    # Prepare timeline steps for Order
    timeline_steps = []
    current_step_index = -1
    
    if order:
        # Get logs to find dates
        logs = order.status_logs.all()
        status_dates = {log.to_status: log.created_at for log in logs}
        # Add creation date for Draft/Placed
        status_dates[Order.Status.DRAFT] = order.created_at

        timeline_steps = [
            {"label": "Order Placed", "status": Order.Status.DRAFT, "icon": "inventory", "date": status_dates.get(Order.Status.DRAFT)},
            {"label": "Approved", "status": Order.Status.APPROVED, "icon": "check_circle", "date": status_dates.get(Order.Status.APPROVED)},
            {"label": "Measuring", "status": Order.Status.MEASURING, "icon": "straighten", "date": status_dates.get(Order.Status.MEASURING)},
            {"label": "Fabrication", "status": Order.Status.FABRICATION, "icon": "precision_manufacturing", "date": status_dates.get(Order.Status.FABRICATION)},
            {"label": "Ready", "status": Order.Status.READY, "icon": "inventory_2", "date": status_dates.get(Order.Status.READY)},
            {"label": "Installation", "status": Order.Status.INSTALLATION, "icon": "construction", "date": status_dates.get(Order.Status.INSTALLATION)},
            {"label": "Completed", "status": Order.Status.COMPLETED, "icon": "verified", "date": status_dates.get(Order.Status.COMPLETED)},
        ]
        
        # Determine current index
        for i, step in enumerate(timeline_steps):
            if step["status"] == order.status:
                current_step_index = i
                break
            # Handle Closed status
            if order.status == Order.Status.CLOSED and step["status"] == Order.Status.COMPLETED:
                current_step_index = i
    
    return render(request, "orders/track.html", {
        "query": query,
        "order": order,
        "quotation": quotation if not order else order.quotation,
        "error": error,
        "timeline_steps": timeline_steps,
        "current_step_index": current_step_index,
    })
