"""
Views for public website pages.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from products.models import Product, Category, Project


def home(request):
    """Homepage view."""
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:12]
    categories = Category.objects.filter(is_active=True)
    
    context = {
        "featured_products": featured_products,
        "categories": categories,
    }
    return render(request, "website/home.html", context)


def products(request):
    """Products listing page."""
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)
    
    # Filter by category if specified
    category_slug = request.GET.get("category")
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)
    
    context = {
        "categories": categories,
        "products": products,
        "selected_category": selected_category,
    }
    return render(request, "website/products.html", context)


def product_detail(request, slug):
    """Single product detail page."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]
    
    context = {
        "product": product,
        "related_products": related_products,
    }
    return render(request, "website/product_detail.html", context)


def portfolio(request):
    """Portfolio/gallery page."""
    projects = Project.objects.all()
    
    # Get unique categories
    categories = sorted(list(set(Project.objects.values_list('category', flat=True))))
    
    context = {
        "projects": projects,
        "categories": categories,
    }
    return render(request, "website/portfolio.html", context)


def about(request):
    """About us page."""
    return render(request, "website/about.html")



from .models import ContactEnquiry

def contact(request):
    """Contact page with enquiry form."""
    if request.method == "POST":
        # Handle form submission
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        
        if name and email and message:
            try:
                # Save to Database
                enquiry = ContactEnquiry.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    message=message
                )

                # Construct email content
                subject = f"New Enquiry from {name}"
                email_message = f"""
                New Enquiry Received:
                
                Name: {name}
                Email: {email}
                Phone: {phone}
                
                Message:
                {message}
                """
                
                # Send email to admin (using default from_email or configured admin)
                from django.core.mail import send_mail
                from django.conf import settings
                
                # Send to admins/support email
                recipient_list = [settings.CONTACT_EMAIL] 
                
                from core.utils import send_background_email
                
                send_background_email(
                    subject=subject,
                    message=email_message,
                    from_email=None, 
                    recipient_list=recipient_list,
                    fail_silently=False,
                )
                
                # Send confirmation to user
                send_background_email(
                    subject="We received your enquiry - Ansari Aluminium",
                    message=f"Hi {name},\n\nThank you for contacting us. We have received your message and will get back to you shortly.\n\nBest Regards,\nAnsari Aluminium Team",
                    from_email=None,
                    recipient_list=[email],
                    fail_silently=True,
                )
                
                messages.success(request, "Thank you! Your message has been sent successfully.")
                return redirect('website:contact')
            except Exception as e:
                # Log error in production
                print(f"Error processing enquiry: {e}")
                messages.error(request, "Something went wrong sending your message. Please try again later.")
        else:
            messages.error(request, "Please fill in all required fields.")
    
    return render(request, "website/contact.html")


def privacy_policy(request):
    """Privacy Policy page."""
    return render(request, "website/privacy_policy.html")


def terms(request):
    """Terms of Service page."""
    return render(request, "website/terms.html")


def sitemap(request):
    """Sitemap page."""
    return render(request, "website/sitemap.html")

