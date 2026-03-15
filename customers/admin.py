"""
Admin configuration for customers app.
"""
from django.contrib import admin
from .models import Customer, SiteLocation


class SiteLocationInline(admin.TabularInline):
    model = SiteLocation
    extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["contact_person", "company_name", "email", "phone", "city", "is_active", "created_at"]
    list_filter = ["is_active", "city", "state"]
    search_fields = ["contact_person", "company_name", "email", "phone", "gst_number"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [SiteLocationInline]
    
    fieldsets = (
        ("Basic Info", {"fields": ("user", "company_name", "contact_person")}),
        ("Contact", {"fields": ("email", "phone", "alternate_phone")}),
        ("Address", {"fields": ("address", "city", "state", "pincode")}),
        ("Business", {"fields": ("gst_number", "notes", "is_active")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
