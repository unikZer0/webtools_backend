from PIL import Image
import pillow_heif
import os

# Register HEIF opener
pillow_heif.register_heif_opener()

def convert_image(input_path: str, output_path: str, output_format: str = "PNG"):
    """
    Converts an image at input_path to the specified output_format and saves it to output_path.
    """
    try:
        with Image.open(input_path) as img:
            # Convert to RGBA ensuring compatibility (some formats like jpeg don't support RGBA, but PNG does)
            # If target is JPEG, we might need RGB. The user specifically asked for PNG.
            if output_format.upper() == "PNG":
                img = img.convert("RGBA")
            elif output_format.upper() == "JPEG":
                img = img.convert("RGB")
                
            img.save(output_path, output_format)
            return True, None
    except Exception as e:
        print(f"Error converting {input_path}: {e}")
        return False, str(e)
