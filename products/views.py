"""
Product catalog views.
"""
from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_list(request):
    """List all products."""
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)
    
    category_slug = request.GET.get("category")
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)
    
    return render(request, "products/list.html", {
        "categories": categories,
        "products": products,
        "selected_category": selected_category,
    })


def category_detail(request, slug):
    """View products by category."""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True)
    
    return render(request, "products/category.html", {
        "category": category,
        "products": products,
    })


def product_detail(request, slug):
    """Single product detail."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]
    
    return render(request, "products/detail.html", {
        "product": product,
        "related_products": related,
    })
