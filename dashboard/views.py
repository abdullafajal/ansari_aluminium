"""
Dashboard views with analytics.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta

from orders.models import Order
from quotations.models import Quotation
from billing.models import Invoice, Payment
from billing.models import Invoice, Payment
from customers.models import Customer
from website.models import ContactEnquiry
from django.db.models import Q


@login_required
def index(request):
    """Main dashboard view."""
    user = request.user
    today = timezone.now().date()
    month_start = today.replace(day=1)
    
    # Different data for admin vs customer
    if user.is_admin:
        # Admin dashboard data
        context = get_admin_dashboard_data(today, month_start)
    else:
        # Customer dashboard data
        context = get_customer_dashboard_data(user, today)
    
    context["user"] = user
    return render(request, "dashboard/index.html", context)


def get_admin_dashboard_data(today, month_start):
    """Get dashboard data for admin users."""
    # Summary stats
    total_orders = Order.objects.count()
    active_orders = Order.objects.filter(
        status__in=[Order.Status.APPROVED, Order.Status.MEASURING, Order.Status.FABRICATION, Order.Status.READY, Order.Status.INSTALLATION]
    ).count()
    
    # Monthly revenue
    monthly_payments = Payment.objects.filter(
        payment_date__gte=month_start
    ).aggregate(total=Sum("amount"))["total"] or 0
    
    # Pending payments
    pending_invoices = Invoice.objects.exclude(
        status__in=[Invoice.Status.PAID, Invoice.Status.CANCELLED]
    )
    pending_amount = sum(inv.balance_due for inv in pending_invoices)
    
    # Recent orders
    recent_orders = Order.objects.select_related("quotation__customer")[:5]
    
    # Pending quotations
    pending_quotes = Quotation.objects.filter(status=Quotation.Status.SENT)[:5]
    
    # Customer count
    total_customers = Customer.objects.filter(is_active=True).count()
    
    # New Enquiries count
    new_enquiries_count = ContactEnquiry.objects.filter(status=ContactEnquiry.Status.NEW).count()
    
    return {
        "total_orders": total_orders,
        "active_orders": active_orders,
        "monthly_revenue": monthly_payments,
        "pending_amount": pending_amount,
        "total_customers": total_customers,
        "recent_orders": recent_orders,
        "pending_quotes": pending_quotes,
        "new_enquiries_count": new_enquiries_count,
        "is_admin_view": True,
    }


def get_customer_dashboard_data(user, today):
    """Get dashboard data for customer users."""
    # Try to get customer profile
    customer = getattr(user, "customer_profile", None)
    
    if customer:
        my_orders = Order.objects.filter(quotation__customer=customer)[:5]
        my_quotations = Quotation.objects.filter(customer=customer)[:5]
        my_invoices = Invoice.objects.filter(order__quotation__customer=customer)[:5]
        active_orders_count = Order.objects.filter(
            quotation__customer=customer
        ).exclude(status__in=[Order.Status.COMPLETED, Order.Status.CLOSED]).count()
    else:
        my_orders = []
        my_quotations = []
        my_invoices = []
        active_orders_count = 0
    
    return {
        "customer": customer,
        "my_orders": my_orders,
        "my_quotations": my_quotations,
        "my_invoices": my_invoices,
        "active_orders_count": active_orders_count,
        "is_admin_view": False,
    }

@login_required
def enquiry_list(request):
    """List all website enquiries."""
    if not request.user.is_admin:
        messages.error(request, "Access denied.")
        return redirect('dashboard:index')
        
    status_filter = request.GET.get('status')
    search_query = request.GET.get('q')
    
    enquiries = ContactEnquiry.objects.all()
    
    if status_filter:
        enquiries = enquiries.filter(status=status_filter)
        
    if search_query:
        enquiries = enquiries.filter(
            Q(name__icontains=search_query) | 
            Q(email__icontains=search_query) | 
            Q(phone__icontains=search_query)
        )
        
    context = {
        "enquiries": enquiries,
        "current_status": status_filter,
        "search_query": search_query,
        "Status": ContactEnquiry.Status,
        "new_enquiries_count": ContactEnquiry.objects.filter(status=ContactEnquiry.Status.NEW).count(),
    }
    return render(request, "dashboard/enquiries/list.html", context)

@login_required
def enquiry_detail(request, pk):
    """View enquiry details."""
    if not request.user.is_admin:
        messages.error(request, "Access denied.")
        return redirect('dashboard:index')
        
    enquiry = get_object_or_404(ContactEnquiry, pk=pk)
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "update_status":
            new_status = request.POST.get("status")
            if new_status:
                enquiry.status = new_status
                enquiry.save()
                messages.success(request, f"Status updated to {enquiry.get_status_display()}")
                
        elif action == "add_note":
            note = request.POST.get("note")
            if note:
                timestamp = timezone.now().strftime("%Y-%m-%d %H:%M")
                current_notes = enquiry.notes or ""
                enquiry.notes = f"{current_notes}\n[{timestamp}] {note}".strip()
                enquiry.save()
                messages.success(request, "Note added successfully")
                
        return redirect('dashboard:enquiry_detail', pk=pk)
        
    context = {
        "enquiry": enquiry,
        "Status": ContactEnquiry.Status,
        "new_enquiries_count": ContactEnquiry.objects.filter(status=ContactEnquiry.Status.NEW).count(),
    }
    return render(request, "dashboard/enquiries/detail.html", context)
