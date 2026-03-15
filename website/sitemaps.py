from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from products.models import Product

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return [
            'website:home',
            'website:about',
            'website:contact',
            'website:portfolio',
            'website:products',
            'website:privacy_policy',
            'website:terms',
            'orders:track',
        ]

    def location(self, item):
        return reverse(item)

class ProductSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at
