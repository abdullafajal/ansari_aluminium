"""
Customer and Address models for customer management.
"""
from django.conf import settings
from django.db import models


class Customer(models.Model):
    """Customer model linked to User account."""
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customer_profile"
    )
    # Company info
    company_name = models.CharField(max_length=200, blank=True)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    alternate_phone = models.CharField(max_length=15, blank=True)
    gst_number = models.CharField(max_length=15, blank=True, verbose_name="GST Number")
    
    # Primary address
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    
    # Additional
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
    
    def __str__(self):
        # Show contact person name with phone - company name in parentheses if exists
        company = self.company_name or ""
        contact = self.contact_person or "Unknown"
        phone = self.phone or ""
        
        parts = []
        if contact != "Unknown":
            parts.append(contact)
        if company:
            parts.append(f"({company})")
            
        base = " ".join(parts) if parts else "Unknown Customer"
        
        if phone:
            return f"{base} - {phone}"
        return base
    
    @property
    def full_address(self):
        """Return formatted full address."""
        return f"{self.address}, {self.city}, {self.state} - {self.pincode}"
    
    @property
    def total_orders(self):
        """Count of all orders for this customer."""
        return self.orders.count()
    
    @property
    def pending_amount(self):
        """Total unpaid amount across all invoices."""
        from billing.models import Invoice
        invoices = Invoice.objects.filter(order__quotation__customer=self)
        return sum(inv.balance_due for inv in invoices)


class SiteLocation(models.Model):
    """Additional site/installation locations for a customer."""
    
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="site_locations"
    )
    name = models.CharField(max_length=100, help_text="e.g., Main Office, Warehouse")
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    contact_person = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Site Location"
        verbose_name_plural = "Site Locations"
    
    def __str__(self):
        return f"{self.customer} - {self.name}"
