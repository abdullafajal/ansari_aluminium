from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import requests
from django.utils.text import slugify
from products.models import Project
from datetime import date

class Command(BaseCommand):
    help = 'Populate database with portfolio projects'

    def handle(self, *args, **options):
        self.stdout.write('Populating portfolio...')

        portfolio_data = [
            {
                "title": "Skyline Apartments Facade",
                "category": "Commercial",
                "location": "Downtown, Dubai",
                "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070&auto=format&fit=crop",
                "date": date(2025, 11, 15)
            },
            {
                "title": "Modern Villa Windows",
                "category": "Residential",
                "location": "Palm Jumeirah",
                "image_url": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?q=80&w=2053&auto=format&fit=crop",
                 "date": date(2025, 10, 20)
            },
            {
                "title": "Corporate Office Partitions",
                "category": "Interiors",
                "location": "Business Bay",
                "image_url": "https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=2069&auto=format&fit=crop",
                 "date": date(2025, 9, 5)
            },
            {
                "title": "Luxury Balcony Enclosure",
                "category": "Residential",
                "location": "Marina Heights",
                "image_url": "https://images.unsplash.com/photo-1628744876497-eb30460be9f6?q=80&w=2070&auto=format&fit=crop",
                 "date": date(2025, 8, 12)
            },
            {
                "title": "Retail Storefront Glazing",
                "category": "Commercial",
                "location": "Mall of Emirates",
                "image_url": "https://images.unsplash.com/photo-1556742502-ec7c0e9f34b1?q=80&w=1974&auto=format&fit=crop",
                 "date": date(2025, 7, 30)
            },
            {
                "title": "Minimalist Home Interior",
                "category": "Interiors",
                "location": "Arabian Ranches",
                "image_url": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?q=80&w=1974&auto=format&fit=crop",
                 "date": date(2025, 6, 18)
            }
        ]

        for item in portfolio_data:
            slug = slugify(item['title'])
            if Project.objects.filter(slug=slug).exists():
                self.stdout.write(f"Project {item['title']} already exists.")
                continue

            project = Project(
                title=item['title'],
                slug=slug,
                category=item['category'],
                location=item['location'],
                date_completed=item['date']
            )

            # Download Image
            self.stdout.write(f"Downloading image for {project.title}...")
            try:
                response = requests.get(item['image_url'], timeout=10)
                if response.status_code == 200:
                    file_name = f"portfolio_{slug}.jpg"
                    project.image.save(file_name, ContentFile(response.content), save=False)
                    project.save()
                    self.stdout.write(self.style.SUCCESS(f'Created project: {project.title}'))
                else:
                    self.stdout.write(self.style.WARNING(f"Failed to download image for {project.title}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating {project.title}: {e}"))
