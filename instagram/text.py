
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image, ImageDraw, ImageFont, ImageEnhance



def wrap_text(text: str, max_width: int, font: ImageFont):
    lines = []
    words = text.split(' ')
     
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        line_width = font.getlength(test_line)
        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line[:-1])
            current_line = word + ' '
 
    lines.append(current_line[:-1])
    return lines


def add_text_to_image(image: Image, text: str, font_path: str, color: str):
     
    # Load a suitable font with the desired size
    font_size = 85
    font = ImageFont.truetype(font_path, font_size)
    
     # Check if the font has a bold variant
    try:
        bold_font_path = font_path.replace('.ttf', '-Bold.ttf')
        font = ImageFont.truetype(bold_font_path, font_size)
    except OSError:
        font = font  # Use the original font if bold variant is not found
        
        
    # Apply line wrap if the text is longer than the image width
    max_width = int(image.width * 0.85)
    wrapped_text = wrap_text(text, max_width, font)
     
    draw = ImageDraw.Draw(image)
    line_spacing = 1.3  # Adjust this value based on your needs
    x = (image.width - max_width) // 2
    y = (image.height - int(font_size * len(wrapped_text) * line_spacing)) // 2
     
    for line in wrapped_text:
        line_width = font.getlength(line)
        draw.text(((image.width - line_width) // 2, y), line, color, font=font)
        y += int(font_size * line_spacing)
        

    return image


def add_image_text(image_path: str = 'test.png', text: str = 'From every experience, extract wisdom, for in its soil blooms the flower of personal growth.', font_path: str = 'JosefinSans-Light.ttf', color: str = 'white', desaturated: bool = True ):
    # Open an image file
    image = Image.open(image_path)

    # Create a drawing object
    draw = ImageDraw.Draw(image)
    
    if desaturated: 
        # Remove saturation
        enhancer = ImageEnhance.Color(image)
        desaturated_image = enhancer.enhance(0)  # 0 means no color, 1 means original color

        # Adjust brightness
        brightness_factor = 0.5  # You can adjust this value as needed
        brightness_enhancer = ImageEnhance.Brightness(desaturated_image)
        image = brightness_enhancer.enhance(brightness_factor)
    
    # Fit text within the image
    image_with_text = add_text_to_image(image.copy(), text, font_path, color)
    
    # Save or display the modified image
    output_path = image_path.replace('.png', '_text.png')
    image_with_text.save(output_path)
    image_with_text.show()
    
    
if __name__ == "__main__":
    add_image_text()