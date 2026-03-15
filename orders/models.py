"""
Order management models with status tracking.
"""
from django.conf import settings
from django.db import models
from django.utils import timezone

from quotations.models import Quotation


def generate_order_number():
    """Generate unique order number."""
    from datetime import datetime
    prefix = datetime.now().strftime("ORD-%Y%m-")
    last = Order.objects.filter(order_number__startswith=prefix).order_by('-order_number').first()
    if last:
        num = int(last.order_number.split('-')[-1]) + 1
    else:
        num = 1
    return f"{prefix}{num:04d}"


class Technician(models.Model):
    """Technician/installer for orders."""
    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    speciality = models.CharField(max_length=100, blank=True, help_text="e.g., UPVC, Aluminium, Glass")
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["name"]
        verbose_name = "Technician"
        verbose_name_plural = "Technicians"
    
    def __str__(self):
        return self.name
    
    @property
    def active_orders(self):
        return self.orders.exclude(status__in=[Order.Status.COMPLETED, Order.Status.CLOSED]).count()


class Order(models.Model):
    """Order created from quotation."""
    
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        APPROVED = "approved", "Approved"
        MEASURING = "measuring", "Measuring"
        FABRICATION = "fabrication", "In Fabrication"
        READY = "ready", "Ready for Installation"
        INSTALLATION = "installation", "Installation in Progress"
        COMPLETED = "completed", "Completed"
        CLOSED = "closed", "Closed"
    
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        NORMAL = "normal", "Normal"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"
    
    order_number = models.CharField(max_length=20, unique=True, default=generate_order_number)
    quotation = models.OneToOneField(
        Quotation,
        on_delete=models.PROTECT,
        related_name="order"
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.NORMAL
    )
    
    # Assignment
    technician = models.ForeignKey(
        Technician,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )
    
    # Dates
    expected_delivery = models.DateField(null=True, blank=True)
    actual_delivery = models.DateField(null=True, blank=True)
    installation_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    
    # Notes
    internal_notes = models.TextField(blank=True, help_text="Internal notes (not visible to customer)")
    customer_notes = models.TextField(blank=True, help_text="Notes visible to customer")
    
    # Tracking
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"
    
    def __str__(self):
        return f"{self.order_number} - {self.quotation.customer}"
    
    @property
    def customer(self):
        return self.quotation.customer
    
    @property
    def total_amount(self):
        return self.quotation.total
    
    @property
    def is_active(self):
        return self.status not in [self.Status.COMPLETED, self.Status.CLOSED]
    
    # Status transition rules (step-by-step)
    STATUS_TRANSITIONS = {
        Status.DRAFT: [Status.APPROVED],
        Status.APPROVED: [Status.MEASURING],
        Status.MEASURING: [Status.FABRICATION],
        Status.FABRICATION: [Status.READY],
        Status.READY: [Status.INSTALLATION],
        Status.INSTALLATION: [Status.COMPLETED],
        Status.COMPLETED: [Status.CLOSED],
        Status.CLOSED: [],
    }
    
    def get_next_statuses(self):
        """Return list of allowed next statuses from current status."""
        return self.STATUS_TRANSITIONS.get(self.status, [])
    
    def can_transition_to(self, new_status):
        """Check if transition to new_status is allowed."""
        return new_status in self.get_next_statuses()
    
    def update_status(self, new_status, user=None, notes=""):
        """Update status and create log entry."""
        if not self.can_transition_to(new_status):
            return False
        
        old_status = self.status
        self.status = new_status
        
        # Set dates based on status
        if new_status == self.Status.COMPLETED:
            self.completed_date = timezone.now().date()
        
        self.save()
        
        # Create log entry
        OrderStatusLog.objects.create(
            order=self,
            from_status=old_status,
            to_status=new_status,
            changed_by=user,
            notes=notes
        )
        
        # Auto-create invoice when order is completed
        if new_status == self.Status.COMPLETED:
            try:
                from billing.models import Invoice
                if not hasattr(self, 'invoice'):
                    Invoice.create_from_order(order=self, user=user)
            except Exception:
                pass  # Invoice creation failed, but order status update succeeded
        
        return True


class OrderStatusLog(models.Model):
    """Log of order status changes."""
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="status_logs"
    )
    from_status = models.CharField(max_length=20)
    to_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order Status Log"
        verbose_name_plural = "Order Status Logs"
    
    def __str__(self):
        return f"{self.order.order_number}: {self.from_status} → {self.to_status}"
    
    @property
    def from_status_display(self):
        """Get human-readable label for from_status."""
        status_dict = dict(Order.Status.choices)
        return status_dict.get(self.from_status, self.from_status)
    
    @property
    def to_status_display(self):
        """Get human-readable label for to_status."""
        status_dict = dict(Order.Status.choices)
        return status_dict.get(self.to_status, self.to_status)

