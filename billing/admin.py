"""
Admin configuration for billing app.
"""
from django.contrib import admin
from .models import Invoice, Payment


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ["created_at"]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "customer", "status", "total", "paid_amount", "balance_due", "due_date", "created_at"]
    list_filter = ["status", "invoice_date", "due_date"]
    search_fields = ["invoice_number", "order__quotation__customer__contact_person"]
    readonly_fields = ["invoice_number", "balance_due", "created_at", "updated_at"]
    inlines = [PaymentInline]
    autocomplete_fields = ["order"]
    
    fieldsets = (
        ("Invoice Info", {"fields": ("invoice_number", "order", "status")}),
        ("Amounts", {"fields": ("subtotal", "discount_amount", "taxable_amount", ("cgst_amount", "sgst_amount"), "total")}),
        ("Payment", {"fields": ("paid_amount", "balance_due")}),
        ("Dates", {"fields": ("invoice_date", "due_date")}),
        ("Notes", {"fields": ("notes",)}),
        ("Tracking", {"fields": ("created_by", "created_at", "updated_at")}),
    )
    
    def customer(self, obj):
        return obj.order.quotation.customer
    customer.short_description = "Customer"
    
    def balance_due(self, obj):
        return obj.balance_due
    balance_due.short_description = "Balance Due"
