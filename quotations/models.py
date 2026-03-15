"""
Quotation models for quote creation and management.
"""
import uuid
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone

from customers.models import Customer
from products.models import Product


def generate_quote_number():
    """Generate unique quotation number."""
    from datetime import datetime
    prefix = datetime.now().strftime("QT-%Y%m-")
    last = Quotation.objects.filter(quote_number__startswith=prefix).order_by('-quote_number').first()
    if last:
        num = int(last.quote_number.split('-')[-1]) + 1
    else:
        num = 1
    return f"{prefix}{num:04d}"


class Quotation(models.Model):
    """Quotation model with line items."""
    
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SENT = "sent", "Sent"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        EXPIRED = "expired", "Expired"
        CONVERTED = "converted", "Converted to Order"
    
    # Public share ID (UUID for sharing without login)
    share_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    quote_number = models.CharField(max_length=20, unique=True, default=generate_quote_number)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="quotations"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    
    # Site info
    site_address = models.TextField(blank=True, help_text="Installation site address if different from customer address")
    
    # Amounts (calculated from items)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    material_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Additional material costs (e.g., for repairs)")
    labour_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Additional labour costs (e.g., for repairs)")
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    taxable_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=18)
    cgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Validity
    valid_until = models.DateField()
    
    # Notes
    notes = models.TextField(blank=True)
    terms = models.TextField(blank=True, default="1. 50% advance payment required.\n2. Delivery within 15 working days.\n3. Installation charges extra.\n4. Quote valid for 15 days only.")
    
    # Tracking
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_quotations"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Quotation"
        verbose_name_plural = "Quotations"
    
    def __str__(self):
        return f"{self.quote_number} - {self.customer}"
    
    def calculate_totals(self):
        """Recalculate all amounts from line items."""
        items = self.items.all()
        items_total = sum(item.amount for item in items)
        
        # Subtotal includes items plus any explicit material and labour costs
        self.subtotal = items_total + self.material_cost + self.labour_cost
        
        # Apply discount
        if self.discount_percent > 0:
            self.discount_amount = (self.subtotal * self.discount_percent) / 100
        self.taxable_amount = self.subtotal - self.discount_amount
        
        # Calculate GST (split into CGST and SGST)
        gst_total = (self.taxable_amount * self.gst_percent) / 100
        self.cgst_amount = gst_total / 2
        self.sgst_amount = gst_total / 2
        
        self.total = self.taxable_amount + gst_total
        self.save()
    
    @property
    def is_expired(self):
        return self.valid_until < timezone.now().date() and self.status == self.Status.SENT
    
    @property
    def can_convert_to_order(self):
        return self.status in [self.Status.SENT, self.Status.ACCEPTED]
    
    @property
    def gst_amount(self):
        """Total GST amount (CGST + SGST)."""
        return self.cgst_amount + self.sgst_amount
    
    # Status transition rules
    STATUS_TRANSITIONS = {
        Status.DRAFT: [Status.SENT],
        Status.SENT: [Status.ACCEPTED, Status.REJECTED, Status.EXPIRED],
        Status.ACCEPTED: [Status.CONVERTED],
        Status.REJECTED: [],
        Status.EXPIRED: [],
        Status.CONVERTED: [],
    }
    
    def get_next_statuses(self):
        """Return list of allowed next statuses from current status."""
        return self.STATUS_TRANSITIONS.get(self.status, [])
    
    def can_transition_to(self, new_status):
        """Check if transition to new_status is allowed."""
        return new_status in self.get_next_statuses()




class QuotationItem(models.Model):
    """Line items in a quotation."""
    
    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    description = models.CharField(max_length=300)
    
    # Measurements
    width = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Width in feet")
    height = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Height in feet")
    
    # Pricing
    quantity = models.DecimalField(max_digits=8, decimal_places=2, default=1)
    unit = models.CharField(max_length=20, default="nos")
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Order
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ["order"]
        verbose_name = "Quotation Item"
        verbose_name_plural = "Quotation Items"
    
    def __str__(self):
        return f"{self.quotation.quote_number} - {self.description}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate amount
        if self.width and self.height:
            area = self.width * self.height
            self.amount = area * self.quantity * self.rate
        else:
            self.amount = self.quantity * self.rate
        super().save(*args, **kwargs)
