from PIL import Image
import math

def process_logo(input_path, output_dir):
    # Load image
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()
    
    new_data = []
    
    # Target Colors for Dark Premium Theme
    cream = (245, 240, 232)     # #F5F0E8
    gold = (212, 168, 83)       # #D4A853
    
    for item in datas:
        r, g, b, a = item
        
        # 1. Calculate Alpha based on "whiteness" (Simple brightness)
        # Assuming background is white (255, 255, 255)
        # Darker pixels = More Opaque. Lighter pixels = More Transparent.
        brightness = (r + g + b) / 3
        
        if brightness > 230:
            # High threshold to remove all off-white artifacts from AI generation
            # so they don't mess up the bounding box centering.
            new_data.append((255, 255, 255, 0))
            continue
            
        # Calculate soft alpha for edges
        # Map brightness 230..0 to alpha 0..255
        alpha = int((230 - brightness) / 230 * 255)
        # Boost alpha slightly to make it solid faster
        alpha = min(255, int(alpha * 1.5))
        
        # 2. Determine Color
        
        # "Gold/Yellowish" check
        # Gold has high Red and Green, low Blue
        if r > b + 30 and g > b + 30:
             # It's Gold -> Change to exact theme Gold
             new_data.append(gold + (alpha,))
        else:
             # It's Light (Cream/Gray) -> Change to exact theme Cream
             new_data.append(cream + (alpha,))

    img.putdata(new_data)
    
    # Crop to content
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    
    # Save original processed version for website header
    # Increase web size resolution for sharper retina display
    aspect = img.width / img.height
    web_h = 240 # @3x (was 160)
    web_w = int(web_h * aspect)
    web_logo = img.resize((web_w, web_h), Image.Resampling.LANCZOS)
    web_logo.save(f"{output_dir}/logo-cream-gold.png")
    print("Saved logo-cream-gold.png")
    
    # Resize and save icons for PWA
    # For PWA, we want White Logo on Brand Navy Background with Rounded Corners
    
    # 1. Get data from the CROPPED image (img)
    cropped_data = img.getdata()
    
    # 2. Create White version of the logo
    white_data = []
    for item in cropped_data:
        r, g, b, a = item
        if a == 0:
            white_data.append((255, 255, 255, 0))
        else:
            white_data.append((255, 255, 255, a))
            
    img_white = Image.new("RGBA", img.size)
    img_white.putdata(white_data)

    sizes = [(512, "icon-512x512.png"), (192, "icon-192x192.png")]
    
    from PIL import ImageDraw
    
    for size, name in sizes:
        # Create Transparent Canvas
        icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        
        # Draw Rounded Navy Blue Square
        draw = ImageDraw.Draw(icon)
        
        # Corner radius (approx 22% is standard for iOS-like squircle look)
        radius = int(size * 0.22)
        
        # Draw navy rounded rect
        draw.rounded_rectangle([(0, 0), (size, size)], radius=radius, fill=(15, 15, 26)) # Hardcode Charcoal for background
        
        # Resize white logo to fit with padding
        padding = int(size * 0.25) 
        target_w = size - (padding * 2)
        target_h = size - (padding * 2)
        
        if aspect > 1: # Wide
            new_w = target_w
            new_h = int(target_w / aspect)
        else: # Tall
            new_h = target_h
            new_w = int(target_h * aspect)
            
        resized_logo = img_white.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Center paste (using logo transparency as mask)
        x = (size - new_w) // 2
        y = (size - new_h) // 2
        
        icon.paste(resized_logo, (x, y), resized_logo)
        
        try:
            icon.save(f"{output_dir}/{name}")
            print(f"Saved {name}")
        except Exception as e:
            print(f"Error saving {name}: {e}")

process_logo(
    '/Users/aqib/.gemini/antigravity/brain/d6685e69-d6fa-42af-be55-b1b0e734538e/ansari_aluminium_logo_cream_gold_1773567139847.png', 
    '/Users/aqib/work/ansari_aluminium/static/assets/icons'
)
