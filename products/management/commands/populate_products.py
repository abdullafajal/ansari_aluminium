from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import requests
from django.utils.text import slugify
from products.models import Category, Product

class Command(BaseCommand):
    help = 'Populate database with initial products data'

    def handle(self, *args, **options):
        self.stdout.write('Populating products...')

        # Categories Data
        categories_data = [
            {
                "name": "Windows",
                "icon": "window",
                "slug": "windows",
                "description": "Premium UPVC and Aluminium windows for every home."
            },
            {
                "name": "Doors",
                "icon": "door_front",
                "slug": "doors",
                "description": "Elegant and secure entryways and balcony doors."
            },
            {
                "name": "Balcony Solutions",
                "icon": "balcony", 
                "slug": "balcony-solutions",
                "description": "Complete balcony covering and safety solutions."
            },
            {
                "name": "Glass & Partitions",
                "icon": "grid_view", # improved icon
                "slug": "glass-partitions",
                "description": "Modern glass partitions, shower cubicles, and spider glazing."
            },
            {
                "name": "Wall & Ceiling Decor",
                "icon": "wallpaper",
                "slug": "wall-ceiling-decor",
                "description": "Decorative profiles, louvers, and panels."
            },
             {
                "name": "Safety & Mesh",
                "icon": "shield",
                "slug": "safety-mesh",
                "description": "Mosquito nets and safety grills."
            }
        ]

        # Products Data
        products_data = [
            # Windows
            {
                "name": "UPVC Sliding Window",
                "category": "windows",
                "base_price": 450.00,
                "unit": "sqft",
                "description": "Classic sliding windows with smooth operation and excellent insulation.",
                "specs": {"Glass": "5mm/6mm Toughened", "Profile": "Multichamber UPVC", "Mesh": "SS 304 (Optional)"},
                "image_url": "https://images.unsplash.com/photo-1503708928676-1cb796a0891e?q=80&w=1974&auto=format&fit=crop"
            },
            {
                "name": "Casement Window",
                "category": "windows",
                "base_price": 550.00,
                "unit": "sqft",
                "description": "Side-hung windows that offer maximum ventilation and clear views.",
                "specs": {"Glass": "Double Glazing Available", "Hinges": "Friction Stays", "Lock": "Multi-point"},
                "image_url": "https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6?q=80&w=2070&auto=format&fit=crop"
            },
            {
                "name": "Tilt & Turn Window",
                "category": "windows",
                "base_price": 850.00,
                "unit": "sqft",
                "description": "Versatile european style windows that tilt for ventilation and turn for cleaning.",
                "specs": {"Hardware": "German Roto/Siegenia", "Glass": "DGU Recommended", "Sound Proofing": "Excellent"},
                "image_url": "https://images.unsplash.com/photo-1516455590571-18256e5bb9ff?q=80&w=1968&auto=format&fit=crop"
            },
            
            # Doors
            {
                "name": "UPVC Sliding Door",
                "category": "doors",
                "base_price": 500.00,
                "unit": "sqft",
                "description": "Large span sliding doors for balconies and patios.",
                "specs": {"Track": "2/3 Track", "Glass": "6mm - 12mm", "Threshold": "Low/Flush"},
                "image_url": "https://images.unsplash.com/photo-1600607686527-6fb886090705?q=80&w=2066&auto=format&fit=crop"
            },
            {
                "name": "Slide & Fold Door",
                "category": "doors",
                "base_price": 1200.00,
                "unit": "sqft",
                "description": "Bi-fold doors that open up the entire wall for seamless indoor-outdoor living.",
                "specs": {"Max Width": "6 Meters", "Operation": "Top/Bottom Rolling", "Glass": "Toughened Only"},
                "image_url": "https://images.unsplash.com/photo-1600566752355-35792bedcfe1?q=80&w=2000&auto=format&fit=crop"
            },
            
            # Balcony
            {
                "name": "Full Balcony Covering",
                "category": "balcony-solutions",
                "base_price": 650.00,
                "unit": "sqft",
                "description": "Completely enclose your balcony with UPVC framing and glass/panels to protect from dust and rain.",
                "specs": {"Roof": "Not Included", "Structure": "Reinforced UPVC", "Warranty": "10 Years"},
                "image_url": "https://images.unsplash.com/photo-1628744876497-eb30460be9f6?q=80&w=2070&auto=format&fit=crop",
                "is_featured": True
            },
            
            # Glass
            {
                "name": "Frameless Shower Cubicle",
                "category": "glass-partitions",
                "base_price": 18000.00,
                "unit": "set",
                "description": "Premium frameless glass shower enclosures with high-quality fittings.",
                "specs": {"Glass": "10mm Toughened", "Hardware": "SS 304 Chrome/Black", "Shape": "L-Shape / Corner"},
                "image_url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?q=80&w=2070&auto=format&fit=crop"
            },
            {
                "name": "Office Glass Partition",
                "category": "glass-partitions",
                "base_price": 350.00,
                "unit": "sqft",
                "description": "Toughened glass partitions for modern office cabins and meeting rooms.",
                "specs": {"Glass": "12mm Toughened", "Profile": "Slim Aluminium", "Door": "Patch Fitting / Stile"},
                "image_url": "https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=2069&auto=format&fit=crop"
            },

            # Decor
            {
                "name": "WPC Louvers",
                "category": "wall-ceiling-decor",
                "base_price": 180.00,
                "unit": "sqft",
                "description": "Wood Plastic Composite louvers for exterior elevation and interior highlight walls.",
                "specs": {"Material": "WPC", "Texture": "Wood Grain", "Application": "Indoor/Outdoor"},
                "image_url": "https://images.unsplash.com/photo-1615873968403-89e068629265?q=80&w=1932&auto=format&fit=crop"
            },
            
            # Safety
            {
                "name": "Safety Jali Door",
                "category": "safety-mesh",
                "base_price": 550.00,
                "unit": "sqft",
                "description": "Heavy duty safety door with SS mesh for security and ventilation.",
                "specs": {"Mesh": "SS 304 High Gauge", "Frame": "UPVC/Aluminium", "Grill": "Optional"},
                "image_url": "https://images.unsplash.com/photo-1595846519845-68e298c2edd8?q=80&w=1887&auto=format&fit=crop"
            }
        ]

        # Create Categories
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'icon': cat_data['icon'],
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # Create Products
        for prod_data in products_data:
            try:
                category = Category.objects.get(slug=prod_data['category'])
                
                # Check if product exists
                slug = slugify(prod_data['name'])
                if Product.objects.filter(slug=slug).exists():
                    self.stdout.write(f"Product {prod_data['name']} already exists.")
                    continue

                product = Product(
                    name=prod_data['name'],
                    slug=slug,
                    category=category,
                    base_price=prod_data['base_price'],
                    unit=prod_data['unit'],
                    description=prod_data['description'],
                    specifications=prod_data['specs'],
                    is_featured=prod_data.get('is_featured', True)
                )

                # Download Image
                if 'image_url' in prod_data:
                    self.stdout.write(f"Downloading image for {product.name}...")
                    try:
                        response = requests.get(prod_data['image_url'], timeout=10)
                        if response.status_code == 200:
                            file_name = f"{slug}.jpg"
                            product.image.save(file_name, ContentFile(response.content), save=False)
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Failed to download image: {e}"))

                product.save()
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
            
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Category {prod_data['category']} not found for {prod_data['name']}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating {prod_data['name']}: {e}"))
