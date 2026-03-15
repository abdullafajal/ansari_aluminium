from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, path):
    # Create a new image with a white background
    img = Image.new('RGB', (size, size), color='#6750A4')
    
    d = ImageDraw.Draw(img)
    
    # Draw a simple "UPVC" text or shape
    # Since we might not have a font, we'll draw a simple house shape
    
    # Coordinates for a house
    padding = size // 4
    points = [
        (size // 2, padding), # Top center
        (padding, size // 2), # Left middle
        (padding, size - padding), # Left bottom
        (size - padding, size - padding), # Right bottom
        (size - padding, size // 2), # Right middle
    ]
    
    d.polygon(points, fill='white', outline='white')
    
    # Save
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    print(f"Created icon at {path}")

create_icon(512, '/Users/aqib/work/ansari_aluminium/static/assets/icons/icon-512x512.png')
create_icon(192, '/Users/aqib/work/ansari_aluminium/static/assets/icons/icon-192x192.png')
