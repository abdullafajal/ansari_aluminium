"""
Main URL configuration for ansari_aluminium project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from website.sitemaps import StaticViewSitemap, ProductSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "products": ProductSitemap,
}

from django.views.generic import TemplateView

urlpatterns = [
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("llms.txt", TemplateView.as_view(template_name="llms.txt", content_type="text/plain")),
    path("admin/", admin.site.urls),
    path("", include("website.urls")),
    path("accounts/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("customers/", include("customers.urls")),
    path("products/", include("products.urls")),
    path("quotations/", include("quotations.urls")),
    path("orders/", include("orders.urls")),
    path("billing/", include("billing.urls")),
    path("", include("pwa.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Admin site customization
admin.site.site_header = "Ansari Aluminium Admin"
admin.site.site_title = "Ansari Aluminium"
admin.site.index_title = "Management Dashboard"
