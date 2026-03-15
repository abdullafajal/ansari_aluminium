"""
Forms for customer management.
"""
from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    """Customer creation/edit form."""
    
    class Meta:
        model = Customer
        fields = [
            "company_name", "contact_person", "email", "phone", 
            "alternate_phone", "gst_number", "address", "city", 
            "state", "pincode", "notes"
        ]
        widgets = {
            "company_name": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
                "placeholder": "Company name (optional)"
            }),
            "contact_person": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
                "placeholder": "Contact person name (optional)"
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
                "placeholder": "Email address (optional)"
            }),
            "phone": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
                "placeholder": "Phone number (optional)"
            }),
            "alternate_phone": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
                "placeholder": "Alternate phone (optional)"
            }),
            "gst_number": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
                "placeholder": "GST number (optional)"
            }),
            "address": forms.Textarea(attrs={
                "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
                "placeholder": "Full address (optional)",
                "rows": 3
            }),
            "city": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
                "placeholder": "City (optional)"
            }),
            "state": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
                "placeholder": "State (optional)"
            }),
            "pincode": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
                "placeholder": "Pincode (optional)"
            }),
            "notes": forms.Textarea(attrs={
                "class": "w-full px-4 py-3 rounded-xl border border-outline-variant bg-surface focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-m3",
                "placeholder": "Additional notes (optional)",
                "rows": 3
            }),
        }
