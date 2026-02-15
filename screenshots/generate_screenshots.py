#!/usr/bin/env python3
"""
Generate App Store screenshots for BlitzRead
iPhone 16 Pro Max: 1290x2796 (6.7")
"""
from PIL import Image, ImageDraw, ImageFont
import os

# App Store screenshot size for 6.7" display
WIDTH = 1290
HEIGHT = 2796

# Colors
BG_COLOR = (0, 0, 0)  # Black background
TEXT_COLOR = (255, 255, 255)  # White text
ACCENT_COLOR = (255, 59, 48)  # Red accent (ORP letter)
BUTTON_COLOR = (30, 30, 30)  # Dark gray buttons

def create_base_image():
    """Create base iPhone screen with black background"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    return img

def add_centered_text(draw, y_pos, text, font_size, color=TEXT_COLOR, bold=False):
    """Add centered text at given y position"""
    try:
        if bold:
            font = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", font_size)
        else:
            font = ImageFont.truetype("/System/Library/Fonts/SFNSText.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x_pos = (WIDTH - text_width) // 2
    draw.text((x_pos, y_pos), text, fill=color, font=font)

def add_word_with_orp(draw, y_pos, word, orp_index):
    """Display a word with red ORP letter"""
    try:
        font = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 180)
    except:
        font = ImageFont.load_default()
    
    # Calculate total width
    before = word[:orp_index]
    orp = word[orp_index]
    after = word[orp_index+1:]
    
    before_bbox = draw.textbbox((0, 0), before, font=font)
    orp_bbox = draw.textbbox((0, 0), orp, font=font)
    after_bbox = draw.textbbox((0, 0), after, font=font)
    
    before_width = before_bbox[2] - before_bbox[0]
    orp_width = orp_bbox[2] - orp_bbox[0]
    after_width = after_bbox[2] - after_bbox[0]
    total_width = before_width + orp_width + after_width
    
    # Center the entire word
    start_x = (WIDTH - total_width) // 2
    
    # Draw each part
    draw.text((start_x, y_pos), before, fill=TEXT_COLOR, font=font)
    draw.text((start_x + before_width, y_pos), orp, fill=ACCENT_COLOR, font=font)
    draw.text((start_x + before_width + orp_width, y_pos), after, fill=TEXT_COLOR, font=font)

def add_rounded_button(draw, center_y, text, width=600):
    """Add a rounded button"""
    height = 120
    x = (WIDTH - width) // 2
    y = center_y - height // 2
    radius = 20
    
    # Draw rounded rectangle
    draw.rounded_rectangle([x, y, x + width, y + height], radius=radius, fill=BUTTON_COLOR)
    
    # Add text
    try:
        font = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = x + (width - text_width) // 2
    text_y = y + (height - 48) // 2
    draw.text((text_x, text_y), text, fill=TEXT_COLOR, font=font)

def add_slider(draw, y_pos, value_text):
    """Add a WPM slider visualization"""
    slider_width = 800
    slider_height = 8
    x_start = (WIDTH - slider_width) // 2
    
    # Slider track
    draw.rectangle([x_start, y_pos, x_start + slider_width, y_pos + slider_height], 
                   fill=(50, 50, 50))
    
    # Filled portion (70% for visual)
    filled_width = int(slider_width * 0.7)
    draw.rectangle([x_start, y_pos, x_start + filled_width, y_pos + slider_height], 
                   fill=ACCENT_COLOR)
    
    # Value label above slider
    add_centered_text(draw, y_pos - 100, value_text, 56, TEXT_COLOR, bold=True)

# Screenshot 1: Speed reading in progress
def create_screenshot_1():
    img = create_base_image()
    draw = ImageDraw.Draw(img)
    
    # App title at top
    add_centered_text(draw, 200, "BlitzRead", 64, TEXT_COLOR, bold=True)
    
    # Main word with ORP letter (red)
    add_word_with_orp(draw, 1200, "reading", 2)  # "r" in "reading" is red
    
    # WPM indicator
    add_centered_text(draw, 1500, "350 WPM", 48, (150, 150, 150))
    
    # Progress indicator
    progress_y = 2200
    add_centered_text(draw, progress_y - 80, "42% Complete", 40, (150, 150, 150))
    
    # Progress bar
    bar_width = 800
    bar_height = 12
    x_start = (WIDTH - bar_width) // 2
    draw.rectangle([x_start, progress_y, x_start + bar_width, progress_y + bar_height], 
                   fill=(50, 50, 50))
    draw.rectangle([x_start, progress_y, x_start + int(bar_width * 0.42), progress_y + bar_height], 
                   fill=ACCENT_COLOR)
    
    # Pause button
    add_rounded_button(draw, 2500, "⏸ Pause")
    
    img.save("~/projects/speed-reader/screenshots/1-reading-progress.png".replace("~", os.path.expanduser("~")))
    print("✓ Created screenshot 1: Reading in progress")

# Screenshot 2: Text input screen
def create_screenshot_2():
    img = create_base_image()
    draw = ImageDraw.Draw(img)
    
    # App title
    add_centered_text(draw, 200, "BlitzRead", 64, TEXT_COLOR, bold=True)
    add_centered_text(draw, 320, "Speed Read Anything", 40, (150, 150, 150))
    
    # Text input box visualization
    box_width = 1000
    box_height = 800
    box_x = (WIDTH - box_width) // 2
    box_y = 600
    draw.rounded_rectangle([box_x, box_y, box_x + box_width, box_y + box_height], 
                          radius=20, outline=(80, 80, 80), width=3)
    
    # Sample text inside
    sample_lines = [
        "Paste or type any text",
        "to start speed reading.",
        "",
        "Articles, books, emails,",
        "anything you want to",
        "read faster."
    ]
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/SFNSText.ttf", 38)
    except:
        font = ImageFont.load_default()
    
    y_offset = box_y + 100
    for line in sample_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x_pos = (WIDTH - text_width) // 2
        draw.text((x_pos, y_offset), line, fill=(150, 150, 150), font=font)
        y_offset += 80
    
    # Start button
    add_rounded_button(draw, 1700, "Start Reading")
    
    # Paste button
    add_rounded_button(draw, 1900, "📋 Paste Text")
    
    img.save("~/projects/speed-reader/screenshots/2-text-input.png".replace("~", os.path.expanduser("~")))
    print("✓ Created screenshot 2: Text input screen")

# Screenshot 3: WPM adjustment screen
def create_screenshot_3():
    img = create_base_image()
    draw = ImageDraw.Draw(img)
    
    # Title
    add_centered_text(draw, 200, "BlitzRead", 64, TEXT_COLOR, bold=True)
    add_centered_text(draw, 320, "Customize Your Speed", 40, (150, 150, 150))
    
    # WPM slider
    add_centered_text(draw, 800, "Reading Speed", 48, TEXT_COLOR)
    add_slider(draw, 1000, "450 WPM")
    
    # Speed presets
    preset_y = 1300
    add_centered_text(draw, preset_y, "Quick Presets:", 44, (150, 150, 150))
    
    presets = [
        ("🐢 Beginner", "200 WPM"),
        ("📖 Average", "300 WPM"),
        ("⚡️ Fast", "450 WPM"),
        ("🚀 Expert", "700 WPM")
    ]
    
    button_spacing = 200
    current_y = preset_y + 150
    
    for emoji_label, wpm in presets:
        # Draw preset button with WPM
        height = 100
        width = 900
        x = (WIDTH - width) // 2
        y = current_y - height // 2
        radius = 15
        
        draw.rounded_rectangle([x, y, x + width, y + height], radius=radius, fill=BUTTON_COLOR)
        
        try:
            font = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 42)
        except:
            font = ImageFont.load_default()
        
        # Label on left, WPM on right
        draw.text((x + 50, y + 25), emoji_label, fill=TEXT_COLOR, font=font)
        
        wpm_bbox = draw.textbbox((0, 0), wpm, font=font)
        wpm_width = wpm_bbox[2] - wpm_bbox[0]
        draw.text((x + width - wpm_width - 50, y + 25), wpm, fill=(150, 150, 150), font=font)
        
        current_y += button_spacing
    
    # Start button at bottom
    add_rounded_button(draw, 2500, "Start Reading")
    
    img.save("~/projects/speed-reader/screenshots/3-wpm-adjustment.png".replace("~", os.path.expanduser("~")))
    print("✓ Created screenshot 3: WPM adjustment")

# Screenshot 4: Different word being read
def create_screenshot_4():
    img = create_base_image()
    draw = ImageDraw.Draw(img)
    
    # App title at top
    add_centered_text(draw, 200, "BlitzRead", 64, TEXT_COLOR, bold=True)
    
    # Different word with ORP
    add_word_with_orp(draw, 1200, "technology", 1)  # "e" is red
    
    # WPM indicator
    add_centered_text(draw, 1500, "550 WPM", 48, (150, 150, 150))
    
    # Progress indicator
    progress_y = 2200
    add_centered_text(draw, progress_y - 80, "78% Complete", 40, (150, 150, 150))
    
    # Progress bar
    bar_width = 800
    bar_height = 12
    x_start = (WIDTH - bar_width) // 2
    draw.rectangle([x_start, progress_y, x_start + bar_width, progress_y + bar_height], 
                   fill=(50, 50, 50))
    draw.rectangle([x_start, progress_y, x_start + int(bar_width * 0.78), progress_y + bar_height], 
                   fill=ACCENT_COLOR)
    
    # Control buttons
    add_centered_text(draw, 2400, "Tap to Pause", 40, (150, 150, 150))
    
    img.save("~/projects/speed-reader/screenshots/4-reading-different.png".replace("~", os.path.expanduser("~")))
    print("✓ Created screenshot 4: Different word reading")

if __name__ == "__main__":
    print("Generating App Store screenshots for BlitzRead...")
    print(f"Size: {WIDTH}x{HEIGHT} (iPhone 16 Pro Max - 6.7\")\n")
    
    create_screenshot_1()
    create_screenshot_2()
    create_screenshot_3()
    create_screenshot_4()
    
    print("\n✅ All screenshots generated in ~/projects/speed-reader/screenshots/")
    print("📱 Ready for App Store submission!")
