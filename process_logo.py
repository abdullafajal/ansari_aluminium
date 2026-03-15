from PIL import Image
import math

def process_logo(input_path, output_dir):
    # Load image
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()
    
    new_data = []
    
    # Target Colors
    navy_blue = (15, 44, 89)    # #0F2C59
    bright_red = (222, 27, 27)  # #DE1B1B
    
    for item in datas:
        r, g, b, a = item
        
        # 1. Calculate Alpha based on "whiteness" (Simple brightness)
        # Assuming background is white (255, 255, 255)
        # Darker pixels = More Opaque. Lighter pixels = More Transparent.
        brightness = (r + g + b) / 3
        
        if brightness > 250:
            # Almost pure white -> transparent
            new_data.append((255, 255, 255, 0))
            continue
            
        # Calculate soft alpha for edges
        # Map brightness 250..0 to alpha 0..255
        alpha = int((250 - brightness) / 250 * 255)
        # Boost alpha slightly to make it solid faster
        alpha = min(255, int(alpha * 1.5))
        
        # 2. Determine Color
        
        # "Red-ish" check
        # Red is dominant and significantly brighter than Green/Blue
        if r > g + 30 and r > b + 30:
             # It's Red -> Change to Bright Red
             new_data.append(bright_red + (alpha,))
        else:
             # It's not Red (Blue, Black, Gray) -> Change to Navy Blue
             new_data.append(navy_blue + (alpha,))

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
    web_logo.save(f"{output_dir}/logo-navy-red.png")
    print("Saved logo-navy-red.png")
    
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
        draw.rounded_rectangle([(0, 0), (size, size)], radius=radius, fill=navy_blue)
        
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
    '/Users/aqib/.gemini/antigravity/brain/92dc8e28-2545-4bb9-869c-dcf4c89deecb/uploaded_media_1770735552578.jpg', 
    '/Users/aqib/work/ansari_aluminium/static/assets/icons'
)
