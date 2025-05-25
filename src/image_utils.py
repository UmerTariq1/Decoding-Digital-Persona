import base64

def get_image_base64(image_path):
    """Convert image to base64 for embedding in HTML"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode() 