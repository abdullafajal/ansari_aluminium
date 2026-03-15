"""
Customer management views.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from core.utils import AdminRequiredMixin
from .models import Customer
from .forms import CustomerForm


@login_required
def customer_list(request):
    """List all customers (admin only)."""
    if not request.user.is_admin:
        messages.error(request, "You don't have permission to view this page.")
        return redirect("dashboard:index")
    
    customers = Customer.objects.all()
    
    # Search
    search = request.GET.get("search", "")
    if search:
        customers = customers.filter(
            contact_person__icontains=search
        ) | customers.filter(
            company_name__icontains=search
        ) | customers.filter(
            phone__icontains=search
        )
    
    # Pagination
    paginator = Paginator(customers, 20)
    page = request.GET.get("page", 1)
    customers = paginator.get_page(page)
    
    return render(request, "customers/list.html", {
        "customers": customers,
        "search": search,
    })


@login_required
def customer_create(request):
    """Create new customer."""
    if not request.user.is_admin:
        messages.error(request, "You don't have permission to create customers.")
        return redirect("dashboard:index")
    
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            
            # Check for linked enquiry
            enquiry_id = request.POST.get("enquiry_id") or request.GET.get("enquiry_id")
            if enquiry_id:
                from website.models import ContactEnquiry
                try:
                    enquiry = ContactEnquiry.objects.get(pk=enquiry_id)
                    enquiry.customer = customer
                    enquiry.status = ContactEnquiry.Status.CONVERTED
                    enquiry.save()
                    messages.success(request, f"Enquiry linked to new customer.")
                except ContactEnquiry.DoesNotExist:
                    pass
            
            messages.success(request, f"Customer '{customer}' created successfully!")
            return redirect("customers:detail", pk=customer.pk)
    else:
        # Pre-fill from GET params (e.g. from Enquiry Convert)
        initial_data = {
            "contact_person": request.GET.get("name", ""),
            "email": request.GET.get("email", ""),
            "phone": request.GET.get("phone", ""),
        }
        form = CustomerForm(initial=initial_data)
    
    return render(request, "customers/form.html", {
        "form": form,
        "title": "Add New Customer",
        "enquiry_id": request.GET.get("enquiry_id"),
    })


@login_required
def customer_detail(request, pk):
    """View customer details."""
    customer = get_object_or_404(Customer, pk=pk)
    
    # Check permissions
    if not request.user.is_admin:
        # Customers can only see their own profile
        if not hasattr(request.user, "customer_profile") or request.user.customer_profile != customer:
            messages.error(request, "You don't have permission to view this customer.")
            return redirect("dashboard:index")
    
    orders = customer.quotations.filter(order__isnull=False).select_related("order")[:10]
    quotations = customer.quotations.all()[:10]
    
    return render(request, "customers/detail.html", {
        "customer": customer,
        "orders": orders,
        "quotations": quotations,
    })


@login_required
def customer_edit(request, pk):
    """Edit customer."""
    if not request.user.is_admin:
        messages.error(request, "You don't have permission to edit customers.")
        return redirect("dashboard:index")
    
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer updated successfully!")
            return redirect("customers:detail", pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, "customers/form.html", {
        "form": form,
        "customer": customer,
        "title": f"Edit {customer}",
    })


@login_required
def customer_delete(request, pk):
    """Delete customer."""
    if not request.user.is_admin:
        messages.error(request, "You don't have permission to delete customers.")
        return redirect("dashboard:index")
    
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == "POST":
        customer_name = str(customer)
        customer.delete()
        messages.success(request, f"Customer '{customer_name}' deleted successfully!")
        return redirect("customers:list")
    
    return render(request, "customers/delete.html", {"customer": customer})
