# select_images.py - Standalone image selector
"""
Run this to select images from downloaded ones
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.images.interactive_image_selector import interactive_image_selection

def main():
    print("\n" + "="*70)
    print("🖼️ INTERACTIVE IMAGE SELECTOR")
    print("="*70)
    
    # Find downloaded images
    images_dir = Path("images/fetched")
    if not images_dir.exists():
        print("❌ No images directory found")
        return
    
    images = list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png")) + list(images_dir.glob("*.webp"))
    
    if not images:
        print("❌ No images found in images/fetched/")
        return
    
    print(f"\n📸 Found {len(images)} images")
    
    # Interactive selection
    selected = interactive_image_selection(images)
    
    # Save selection to file
    if selected:
        with open("selected_images.txt", 'w') as f:
            for img in selected:
                f.write(f"{img}\n")
        print(f"\n✅ Saved {len(selected)} selected images to selected_images.txt")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()