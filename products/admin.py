"""
Admin configuration for products app.
"""
from django.contrib import admin
from .models import Category, Product, ProductImage, Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "location", "date_completed", "is_featured"]
    list_filter = ["category", "is_featured", "date_completed"]
    search_fields = ["title", "location", "description"]
    date_hierarchy = "date_completed"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "product_count", "is_active", "order"]
    list_editable = ["order", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "base_price", "unit", "is_featured", "is_active", "order"]
    list_filter = ["category", "is_featured", "is_active"]
    list_editable = ["order", "is_featured", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "description"]
    inlines = [ProductImageInline]
