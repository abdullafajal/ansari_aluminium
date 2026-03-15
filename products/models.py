"""
Product catalog models.
"""
from django.db import models


class Category(models.Model):
    """Product category for organizing products."""
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Material Icon name")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name
    
    @property
    def product_count(self):
        return self.products.filter(is_active=True).count()


class Product(models.Model):
    """Product model for UPVC/Aluminium items."""
    
    class Unit(models.TextChoices):
        SQFT = "sqft", "Square Feet"
        RFT = "rft", "Running Feet"
        NOS = "nos", "Numbers"
        SET = "set", "Set"
    
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    # Pricing
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Base price per unit"
    )
    unit = models.CharField(
        max_length=10,
        choices=Unit.choices,
        default=Unit.SQFT
    )
    
    # Media
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    
    # Specifications
    specifications = models.JSONField(default=dict, blank=True)
    
    # Display
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("website:product_detail", kwargs={"slug": self.slug})


class ProductImage(models.Model):
    """Additional images for a product."""
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="products/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ["order"]
    
    def __str__(self):
        return f"{self.product.name} - Image {self.order}"


class Project(models.Model):
    """Portfolio project showcase."""
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=100, help_text="e.g. Residential, Commercial, Interior")
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="portfolio/")
    date_completed = models.DateField(null=True, blank=True)
    
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["order", "-date_completed"]
    
    def __str__(self):
        return self.title
