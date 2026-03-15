"""
Context processors for global template variables.
"""
from django.conf import settings


def site_settings(request):
    """Add site settings to template context."""
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "Ansari Aluminium"),
        "SITE_TAGLINE": getattr(settings, "SITE_TAGLINE", "Premium Fabrication"),
        "GST_RATE": getattr(settings, "GST_RATE", 18),
        "current_year": __import__("datetime").datetime.now().year,
    }
