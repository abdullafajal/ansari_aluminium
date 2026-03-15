"""
Admin configuration for orders app.
"""
from django.contrib import admin
from .models import Order, OrderStatusLog, Technician


class OrderStatusLogInline(admin.TabularInline):
    model = OrderStatusLog
    extra = 0
    readonly_fields = ["from_status", "to_status", "changed_by", "notes", "created_at"]
    can_delete = False


@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "speciality", "is_active", "active_orders"]
    list_filter = ["is_active", "speciality"]
    search_fields = ["name", "phone"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "customer", "status", "priority", "technician", "expected_delivery", "created_at"]
    list_filter = ["status", "priority", "technician", "created_at"]
    search_fields = ["order_number", "quotation__customer__contact_person"]
    readonly_fields = ["order_number", "created_at", "updated_at"]
    inlines = [OrderStatusLogInline]
    autocomplete_fields = ["quotation", "technician"]
    
    fieldsets = (
        ("Order Info", {"fields": ("order_number", "quotation", "status", "priority")}),
        ("Assignment", {"fields": ("technician",)}),
        ("Dates", {"fields": ("expected_delivery", "actual_delivery", "installation_date", "completed_date")}),
        ("Notes", {"fields": ("internal_notes", "customer_notes")}),
        ("Tracking", {"fields": ("created_by", "created_at", "updated_at")}),
    )
    
    def customer(self, obj):
        return obj.quotation.customer
    customer.short_description = "Customer"
