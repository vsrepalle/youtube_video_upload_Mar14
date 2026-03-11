import os
import json
import shutil
from pathlib import Path
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
from PIL import Image

# --- CONFIG ---
IMAGES_PER_TERM = 1
JSON_FILE = "data.json"
PROJECT_ROOT = Path(__file__).parent.absolute()

def auto_cleanup():
    print("🧹 Running Auto-Cleanup...")
    fetch_dir = PROJECT_ROOT / 'images' / 'fetched'
    if fetch_dir.exists():
        shutil.rmtree(fetch_dir)
    fetch_dir.mkdir(parents=True, exist_ok=True)
    print("✅ Cleanup Complete.")

def process_and_crop():
    """Processes all downloaded images: converts to RGB, crops to 9:16, and renames them."""
    fetch_dir = PROJECT_ROOT / 'images' / 'fetched'
    images = list(fetch_dir.glob("*"))
    
    for i, img_path in enumerate(images):
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
                # Save with a clean index name for the video script to find
                final_img.save(fetch_dir / f"{i}.jpg", "JPEG")
            
            # Remove the original icrawler file if it wasn't named i.jpg
            if img_path.name != f"{i}.jpg":
                img_path.unlink()
        except Exception as e:
            print(f"⚠️ Failed to process {img_path.name}: {e}")

def fetch_with_icrawler():
    if not os.path.exists(JSON_FILE):
        print(f"❌ {JSON_FILE} not found!")
        return

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Accessing the specific path in your JSON
    search_keys = data.get("metadata", {}).get("image_search_keys", [])
    save_dir = str(PROJECT_ROOT / 'images' / 'fetched')

    print(f"🚀 Starting icrawler for {len(search_keys)} terms...")

    for term in search_keys:
        print(f"🔍 Fetching: {term}")
        # Using Bing crawler as it's often more lenient with automated requests
        bing_crawler = BingImageCrawler(storage={'root_dir': save_dir})
        bing_crawler.crawl(keyword=term, max_num=IMAGES_PER_TERM)

    # After downloading, we need to standardize the sizes and names
    process_and_crop()

if __name__ == "__main__":
    auto_cleanup()
    fetch_with_icrawler()