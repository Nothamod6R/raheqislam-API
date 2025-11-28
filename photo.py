from PIL import Image, ImageDraw, ImageFont
import math

# --- Configuration ---
IMAGE_SIZE = (800, 600)  # Width, Height
BACKGROUND_COLORS = {
    'purple': (128, 0, 128),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'blue': (0, 0, 255),
    'red': (255, 0, 0)
}
TEXT_COLOR = (255, 255, 0)  # Bright Yellow for high contrast
FONT_PATH = "arial.ttf"  # Use a common font or specify a path to a custom one
FONT_SIZE = 40
MAX_LINES = 6

def blend_colors(c1, c2, ratio):
    """Blends two RGB colors based on a ratio (0.0 to 1.0)."""
    return tuple(int(a + (b - a) * ratio) for a, b in zip(c1, c2))

def create_radial_gradient_background(width, height, colors):
    """
    Creates an image with a radial gradient using the 5 specified colors.
    The colors are blended from the center outward:
    White -> Blue -> Red -> Purple -> Black
    This design blends the 5 colors creatively as requested.
    """
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    center_x, center_y = width // 2, height // 2
    max_dist = math.hypot(center_x, center_y)

    color_list = [
        colors['white'],
        colors['blue'],
        colors['red'],
        colors['purple'],
        colors['black']
    ]

    num_stops = len(color_list) - 1

    for x in range(width):
        for y in range(height):
            # Calculate distance from the center and normalize it (0.0 to 1.0)
            distance = math.hypot(x - center_x, y - center_y)
            norm_dist = min(1.0, distance / max_dist)

            # Determine which two colors to blend
            stop_index = int(norm_dist * num_stops)
            stop_index = min(stop_index, num_stops - 1)  # Ensure we stay in bounds

            color_a = color_list[stop_index]
            color_b = color_list[stop_index + 1]

            # Calculate the ratio for the blend between the two colors
            segment_start = stop_index / num_stops
            segment_length = 1 / num_stops
            ratio = (norm_dist - segment_start) / segment_length

            pixels[x, y] = blend_colors(color_a, color_b, ratio)

    return img

def generate_text_image(text_input, filename="generated_image.png"):
    """
    Generates the final image with the gradient background and centered text.
    """
    try:
        # --- 1. Text Preparation (Max 6 lines constraint) ---
        # Simple splitting by newline, taking only the first MAX_LINES
        lines = text_input.strip().split('\n')
        if len(lines) > MAX_LINES:
            lines = lines[:MAX_LINES]
            print(f"Warning: Text truncated to {MAX_LINES} lines.")
        
        display_text = "\n".join(lines)

        # --- 2. Image and Drawing Setup ---
        img = create_radial_gradient_background(IMAGE_SIZE[0], IMAGE_SIZE[1], BACKGROUND_COLORS)
        draw = ImageDraw.Draw(img)

        try:
            # Load a TrueType font
            font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        except IOError:
            # Fallback to default font if the specified one isn't found
            print(f"Warning: Could not load '{FONT_PATH}'. Using default font.")
            font = ImageFont.load_default()

        # --- 3. Centering Text Calculation ---
        # Get bounding box (width and height) of the multi-line text
        # Use getbbox for better accuracy in modern Pillow versions
        bbox = draw.textbbox((0, 0), display_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculate coordinates to center the text
        x = (IMAGE_SIZE[0] - text_width) / 2
        y = (IMAGE_SIZE[1] - text_height) / 2

        # --- 4. Draw Text ---
        # Text is drawn with the contrasting color (Yellow) in the center.
        # This ensures the text stands out clearly in the middle.
        draw.text((x, y), display_text, font=font, fill=TEXT_COLOR, align="center")

        # --- 5. Save Image ---
        img.save(filename)
        print(f"Image successfully generated and saved as {filename}!")
        
        # 

    except Exception as e:
        print(f"An error occurred during image generation: {e}")


# --- Application Example Usage ---

user_text = """
This is line one.
Line two is important.
The third line is longer.
Contrast is key!
The text stands out.
Sixth line, the maximum.
This line will be ignored.
"""

generate_text_image(user_text)