"""
Admin configuration for quotations app.
"""
from django.contrib import admin
from .models import Quotation, QuotationItem


class QuotationItemInline(admin.TabularInline):
    model = QuotationItem
    extra = 1
    fields = ["description", "width", "height", "quantity", "unit", "rate", "amount"]
    readonly_fields = ["amount"]


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ["quote_number", "customer", "status", "total", "valid_until", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["quote_number", "customer__contact_person", "customer__company_name"]
    readonly_fields = ["quote_number", "subtotal", "discount_amount", "taxable_amount", "cgst_amount", "sgst_amount", "total", "created_at", "updated_at"]
    inlines = [QuotationItemInline]
    autocomplete_fields = ["customer"]
    
    fieldsets = (
        ("Quote Info", {"fields": ("quote_number", "customer", "status", "site_address")}),
        ("Amounts", {"fields": ("subtotal", ("discount_percent", "discount_amount"), "taxable_amount", ("cgst_amount", "sgst_amount"), "total")}),
        ("Validity", {"fields": ("valid_until",)}),
        ("Notes", {"fields": ("notes", "terms")}),
        ("Tracking", {"fields": ("created_by", "created_at", "updated_at")}),
    )
    
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # Recalculate totals after saving items
        form.instance.calculate_totals()
