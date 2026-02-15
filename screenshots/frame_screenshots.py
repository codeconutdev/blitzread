#!/usr/bin/env python3
"""
Create App Store marketing screenshots from raw simulator captures.
Adds gradient background, marketing headline, and rounded corners.
Output: 1290x2796 (iPhone 6.7" required size)
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'marketing')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# App Store dimensions for 6.7" display
CANVAS_W, CANVAS_H = 1290, 2796

# Marketing text for each screenshot
screens = [
    {
        'file': '06_playing_word2.png',
        'headline': 'Read 3x Faster',
        'subline': 'One word at a time. Laser focus.',
        'bg_top': '#1A0A0A',
        'bg_bottom': '#0A0A1A',
        'accent': '#FF3B30',
    },
    {
        'file': '01_initial.png',
        'headline': 'Paste Any Text',
        'subline': 'Articles, books, emails — speed read anything.',
        'bg_top': '#0A0A1A',
        'bg_bottom': '#1A0A2A',
        'accent': '#FF3B30',
    },
    {
        'file': '03_reading.png',
        'headline': 'Smart Word Timing',
        'subline': 'Longer words linger. Short ones fly.',
        'bg_top': '#0A1A1A',
        'bg_bottom': '#0A0A1A',
        'accent': '#FF3B30',
    },
    {
        'file': '02_with_text.png',
        'headline': 'Built for Focus',
        'subline': 'Dark theme. Zero distractions.',
        'bg_top': '#1A1A0A',
        'bg_bottom': '#0A0A1A',
        'accent': '#FF3B30',
    },
]

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def create_gradient(w, h, top_color, bottom_color):
    img = Image.new('RGB', (w, h))
    draw = ImageDraw.Draw(img)
    r1, g1, b1 = hex_to_rgb(top_color)
    r2, g2, b2 = hex_to_rgb(bottom_color)
    for y in range(h):
        ratio = y / h
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img

def round_corners(img, radius):
    """Add rounded corners to an image"""
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
    result = img.copy()
    result.putalpha(mask)
    return result

def add_shadow(canvas, phone_img, x, y):
    """Add subtle shadow behind phone"""
    shadow = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        [(x+8, y+8), (x + phone_img.width + 8, y + phone_img.height + 8)],
        radius=40, fill=(0, 0, 0, 80)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=15))
    canvas.paste(shadow, (0, 0), shadow)

# Try to find a good font
font_paths = [
    '/System/Library/Fonts/SFPro-Bold.otf',
    '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
    '/System/Library/Fonts/Helvetica.ttc',
]

font_path = None
for fp in font_paths:
    if os.path.exists(fp):
        font_path = fp
        break

for i, screen in enumerate(screens):
    print(f"Creating marketing screenshot {i+1}/{len(screens)}: {screen['headline']}")
    
    # Create gradient background
    canvas = create_gradient(CANVAS_W, CANVAS_H, screen['bg_top'], screen['bg_bottom'])
    canvas = canvas.convert('RGBA')
    
    # Load and resize screenshot
    raw = Image.open(os.path.join(SCRIPT_DIR, screen['file'])).convert('RGBA')
    
    # Scale phone screenshot to fit with padding
    phone_w = int(CANVAS_W * 0.82)
    phone_h = int(raw.height * (phone_w / raw.width))
    raw = raw.resize((phone_w, phone_h), Image.LANCZOS)
    
    # Round the corners of the screenshot
    raw = round_corners(raw, 40)
    
    # Position: centered horizontally, lower portion of canvas
    phone_x = (CANVAS_W - phone_w) // 2
    phone_y = CANVAS_H - phone_h - 80  # 80px from bottom
    
    # Add shadow
    add_shadow(canvas, raw, phone_x, phone_y)
    
    # Paste screenshot
    canvas.paste(raw, (phone_x, phone_y), raw)
    
    # Add headline text
    draw = ImageDraw.Draw(canvas)
    
    if font_path:
        title_font = ImageFont.truetype(font_path, 96)
        sub_font = ImageFont.truetype(font_path, 42)
    else:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
    
    # Headline - centered, near top
    title_y = 180
    bbox = draw.textbbox((0, 0), screen['headline'], font=title_font)
    title_x = (CANVAS_W - (bbox[2] - bbox[0])) // 2
    draw.text((title_x, title_y), screen['headline'], fill='white', font=title_font)
    
    # Subline
    sub_y = title_y + 120
    bbox = draw.textbbox((0, 0), screen['subline'], font=sub_font)
    sub_x = (CANVAS_W - (bbox[2] - bbox[0])) // 2
    draw.text((sub_x, sub_y), screen['subline'], fill=(200, 200, 200), font=sub_font)
    
    # Save
    output = canvas.convert('RGB')
    output.save(os.path.join(OUTPUT_DIR, f'appstore_{i+1}.png'), 'PNG', quality=95)
    print(f"  → Saved appstore_{i+1}.png ({CANVAS_W}x{CANVAS_H})")

print(f"\n✅ Done! {len(screens)} marketing screenshots in {OUTPUT_DIR}")
