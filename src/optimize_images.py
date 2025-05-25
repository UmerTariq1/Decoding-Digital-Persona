from PIL import Image
import os

def optimize_image(input_path, output_path, size=(240, 240), quality=85):
    """Optimize an image by resizing and compressing it."""
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (in case of RGBA)
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            
            # Resize the image
            img = img.resize(size, Image.Resampling.LANCZOS)
            
            # Save the optimized image
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            # Get file sizes
            original_size = os.path.getsize(input_path) / 1024  # KB
            optimized_size = os.path.getsize(output_path) / 1024  # KB
            
            print(f"Original size: {original_size:.1f}KB")
            print(f"Optimized size: {optimized_size:.1f}KB")
            print(f"Reduction: {((original_size - optimized_size) / original_size * 100):.1f}%")
            
    except Exception as e:
        print(f"Error optimizing image: {e}")

if __name__ == "__main__":
    # Optimize the logo
    optimize_image(
        "data/ref_imgs/logo.jpeg",
        "data/ref_imgs/logo_optimized.jpeg"
    ) 