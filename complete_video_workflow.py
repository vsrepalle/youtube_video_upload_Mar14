import os
import json
import shutil
from pathlib import Path
from icrawler.builtin import BingImageCrawler
from PIL import Image

# --- CONFIG ---
IMAGES_PER_TERM = 1
JSON_FILE = "data.json"
PROJECT_ROOT = Path(__file__).parent.absolute()

def auto_cleanup():
    """Skips cleanup to preserve manually picked images."""
    return # skipped
    print("🧹 Running Auto-Cleanup...")
    fetch_dir = PROJECT_ROOT / 'images' / 'fetched'
    if fetch_dir.exists():
        shutil.rmtree(fetch_dir)
    fetch_dir.mkdir(parents=True, exist_ok=True)
    print("✅ Cleanup Complete.")

def process_and_crop():
    """Processes images: converts to RGB, crops to 9:16, and renames them to match scene indices."""
    fetch_dir = PROJECT_ROOT / 'images' / 'fetched'
    # We sort them to ensure 000001.jpg becomes 0.jpg, etc.
    images = sorted(list(fetch_dir.glob("*")))
    
    print("✂️ Standardizing and Cropping images...")
    for i, img_path in enumerate(images):
        # Skip if already named correctly (e.g. 0.jpg) to avoid re-processing
        if img_path.name == f"{i}.jpg":
            continue
            
        try:
            with Image.open(img_path) as img:
                img = img.convert('RGB')
                w, h = img.size
                target_ratio = 1080 / 1920
                current_ratio = w / h

                if current_ratio > target_ratio:
                    new_width = int(h * target_ratio)
                    left = (w - new_width) // 2
                    img = img.crop((left, 0, left + new_width, h))
                else:
                    new_height = int(w / target_ratio)
                    top = (h - new_height) // 2
                    img = img.crop((0, top, w, top + new_height))
                
                final_img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
                # Save as scene index (0.jpg, 1.jpg)
                final_img.save(fetch_dir / f"{i}.jpg", "JPEG")
            
            # Remove the original icrawler file
            img_path.unlink()
            print(f"✅ Processed: {i}.jpg")
        except Exception as e:
            print(f"⚠️ Failed to process {img_path.name}: {e}")

def fetch_with_icrawler():
    if not os.path.exists(JSON_FILE):
        print(f"❌ {JSON_FILE} not found!")
        return

    # Using utf-8-sig to handle PowerShell's BOM
    with open(JSON_FILE, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    # Updated to read from your new 'scenes' list
    search_keys = [s.get("search_key") for s in data.get("scenes", [])]
    save_dir = str(PROJECT_ROOT / 'images' / 'fetched')

    print(f"🚀 Starting icrawler for {len(search_keys)} terms...")

    for term in search_keys:
        print(f"🔍 Checking/Fetching for: {term}")
        bing_crawler = BingImageCrawler(storage={'root_dir': save_dir})
        # Note: icrawler skips existing files by default, preserving your manual picks!
        bing_crawler.crawl(keyword=term, max_num=IMAGES_PER_TERM)

    # Standardize names and crops
    process_and_crop()

if __name__ == "__main__":
    # 1. Fetch/Verify Images
    fetch_with_icrawler()
    
    # 2. TRIGGER VIDEO RENDERING HERE
    print("\n🎬 Images ready. Starting video rendering...")
    
    # If your rendering logic is in another file, you would call it here.
    # For example: 
    # os.system("python render_video_script.py")
    
    print("✨ Workflow complete!")