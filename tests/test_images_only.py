# test_images_only.py
from pathlib import Path
from fetch_images_dynamic import fetch_images_from_json

images = fetch_images_from_json("data.json", num_images=6)

print("\nDownloaded images:")
for img in images:
    print(f" - {img.absolute()} ({img.stat().st_size / 1024:.1f} KB)")

print(f"\nTotal: {len(images)} images")
print("Open them manually to check if they match the story.")

try:
    from PIL import Image
    print("\nBasic preview (image sizes):")
    for img_path in images:
        with Image.open(img_path) as im:
            print(f"   {img_path.name}: {im.size} {im.format}")
except ImportError:
    print("Install Pillow to see image info: pip install pillow")