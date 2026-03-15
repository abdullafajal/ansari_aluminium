"""
Invoice and Payment models for billing.
"""
import uuid
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone

from orders.models import Order


def generate_invoice_number():
    """Generate unique invoice number."""
    from datetime import datetime
    prefix = datetime.now().strftime("INV-%Y%m-")
    last = Invoice.objects.filter(invoice_number__startswith=prefix).order_by('-invoice_number').first()
    if last:
        num = int(last.invoice_number.split('-')[-1]) + 1
    else:
        num = 1
    return f"{prefix}{num:04d}"


class Invoice(models.Model):
    """Invoice generated from Order."""
    
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SENT = "sent", "Sent"
        UNPAID = "unpaid", "Unpaid"
        PARTIAL = "partial", "Partially Paid"
        PAID = "paid", "Paid"
        OVERDUE = "overdue", "Overdue"
        CANCELLED = "cancelled", "Cancelled"
    
    # Public share ID (UUID for sharing without login)
    share_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    invoice_number = models.CharField(max_length=20, unique=True, default=generate_invoice_number)
    order = models.OneToOneField(
        Order,
        on_delete=models.PROTECT,
        related_name="invoice"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    
    # Amounts (copied from quotation for record)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    material_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    labour_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    taxable_amount = models.DecimalField(max_digits=12, decimal_places=2)
    cgst_amount = models.DecimalField(max_digits=12, decimal_places=2)
    sgst_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Payment tracking
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Dates
    invoice_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Tracking
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_invoices"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
    
    def __str__(self):
        return f"{self.invoice_number} - {self.order.customer}"
    
    @property
    def customer(self):
        return self.order.customer
    
    @property
    def balance_due(self):
        return self.total - self.paid_amount
    
    @property
    def is_overdue(self):
        return self.due_date < timezone.now().date() and self.status not in [self.Status.PAID, self.Status.CANCELLED]
    
    def update_payment_status(self):
        """Update status based on paid amount."""
        if self.paid_amount >= self.total:
            self.status = self.Status.PAID
        elif self.paid_amount > 0:
            self.status = self.Status.PARTIAL
        elif self.is_overdue:
            self.status = self.Status.OVERDUE
        elif self.status == self.Status.DRAFT:
            pass  # Keep as draft
        else:
            self.status = self.Status.UNPAID
        self.save()
    
    def add_payment(self, amount, method, reference="", notes="", user=None):
        """Add a payment to this invoice."""
        payment = Payment.objects.create(
            invoice=self,
            amount=amount,
            method=method,
            reference=reference,
            notes=notes,
            received_by=user
        )
        self.paid_amount += Decimal(str(amount))
        self.update_payment_status()
        return payment
    
    @classmethod
    def create_from_order(cls, order, due_days=30, user=None):
        """Create invoice from order."""
        quotation = order.quotation
        
        invoice = cls.objects.create(
            order=order,
            subtotal=quotation.subtotal,
            material_cost=quotation.material_cost,
            labour_cost=quotation.labour_cost,
            discount_amount=quotation.discount_amount,
            taxable_amount=quotation.taxable_amount,
            cgst_amount=quotation.cgst_amount,
            sgst_amount=quotation.sgst_amount,
            total=quotation.total,
            due_date=timezone.now().date() + timezone.timedelta(days=due_days),
            created_by=user,
            status=cls.Status.UNPAID
        )
        return invoice


class Payment(models.Model):
    """Payment record for an invoice."""
    
    class Method(models.TextChoices):
        CASH = "cash", "Cash"
        BANK_TRANSFER = "bank", "Bank Transfer"
        UPI = "upi", "UPI"
        CHEQUE = "cheque", "Cheque"
        CARD = "card", "Card"
        OTHER = "other", "Other"
    
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(
        max_length=20,
        choices=Method.choices,
        default=Method.CASH
    )
    
    # Reference info
    reference = models.CharField(max_length=100, blank=True, help_text="Transaction ID, Cheque number, etc.")
    notes = models.TextField(blank=True)
    
    # Date
    payment_date = models.DateField(default=timezone.now)
    
    # Tracking
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-payment_date", "-created_at"]
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
    
    def __str__(self):
        return f"{self.invoice.invoice_number} - ₹{self.amount}"
