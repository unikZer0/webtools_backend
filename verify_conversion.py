from service.image_service import convert_image
from PIL import Image
import os

# Create a dummy image
img = Image.new('RGB', (60, 30), color = 'red')
img.save('test_input.jpg')

# Test conversion
success, error = convert_image('test_input.jpg', 'test_output.png')

if success and os.path.exists('test_output.png'):
    print("Verification Successful: Image converted to PNG")
    # Clean up
    os.remove('test_input.jpg')
    os.remove('test_output.png')
else:
    print(f"Verification Failed: {error}")
