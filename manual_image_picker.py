import os
import json
import shutil
from pathlib import Path
from icrawler.builtin import BingImageCrawler
from PIL import Image
import time

# --- CONFIG ---
IMAGES_TO_FETCH = 5
PROJECT_ROOT = Path(__file__).parent.absolute()
LIBRARY_ROOT = PROJECT_ROOT / 'content_library'

def auto_cleanup():
    print("🧹 Cleaning temporary selection folders...")
    temp_dir = PROJECT_ROOT / 'images' / 'temp_selection'
    fetch_dir = PROJECT_ROOT / 'images' / 'fetched'
    for d in [temp_dir, fetch_dir]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)
    if not LIBRARY_ROOT.exists():
        LIBRARY_ROOT.mkdir(parents=True)

def save_to_library(img_path, search_term):
    """Saves a copy of the winner to a structured library."""
    parts = search_term.lower().split()
    if len(parts) >= 2:
        category = f"{parts[0]}_{parts[1]}" # e.g., virat_kohli
        action = "_".join(parts[2:]) if len(parts) > 2 else "general"
    else:
        category = parts[0] if parts else "misc"
        action = "general"

    target_dir = LIBRARY_ROOT / category / action
    target_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = int(time.time())
    library_path = target_dir / f"image_{timestamp}.jpg"
    shutil.copy(img_path, library_path)
    print(f"📚 Archived to Library: {category}/{action}")

def manual_selector(term, temp_dir, scene_index):
    time.sleep(1)
    images = list(temp_dir.glob("*"))[:IMAGES_TO_FETCH]
    if not images:
        print(f"⚠️ No images found for: {term}")
        return None

    print(f"\n" + "="*45)
    print(f" 📸 SELECT IMAGE FOR SCENE {scene_index}")
    print(f" Search Term: {term}")
    print(f"="*45)

    for i, img in enumerate(images):
        print(f" [{i+1}] Opening: {img.name}")
        os.startfile(str(img))

    while True:
        choice = input(f"\n👉 Type the number (1-{len(images)}) to pick: ")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(images):
                return images[idx]
        except ValueError:
            print("❌ Invalid input. Use numbers only.")

def process_winner(img_path, save_dir, index, term):
    try:
        # First, archive the raw high-quality original to library
        save_to_library(img_path, term)
        
        # Then, process the crop for the current video
        with Image.open(img_path) as img:
            img = img.convert('RGB')
            w, h = img.size
            target_ratio = 1080 / 1920
            if (w / h) > target_ratio:
                new_width = int(h * target_ratio)
                left = (w - new_width) // 2
                img = img.crop((left, 0, left + new_width, h))
            else:
                new_height = int(w / target_ratio)
                top = (h - new_height) // 2
                img = img.crop((0, top, w, top + new_height))
            
            final_img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
            final_img.save(save_dir / f"{index}.jpg", "JPEG")
            print(f"✅ Processed for video as {index}.jpg")
    except Exception as e:
        print(f"⚠️ Error: {e}")

def run_picker(json_filename):
    if not os.path.exists(json_filename):
        print(f"❌ File {json_filename} not found!")
        return
    with open(json_filename, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)

    scenes = data.get("scenes", [])
    fetch_dir = PROJECT_ROOT / 'images' / 'fetched'
    temp_root = PROJECT_ROOT / 'images' / 'temp_selection'

    for i, scene in enumerate(scenes):
        term = scene.get("search_key", "trending news")
        scene_temp = temp_root / f"scene_{i}"
        scene_temp.mkdir(parents=True, exist_ok=True)
        print(f"\n🔍 Searching Bing for: {term}...")
        bing = BingImageCrawler(storage={'root_dir': str(scene_temp)})
        bing.crawl(keyword=term, max_num=IMAGES_TO_FETCH)
        winner = manual_selector(term, scene_temp, i)
        if winner:
            process_winner(winner, fetch_dir, i, term)

if __name__ == "__main__":
    import sys
    target_json = sys.argv[1] if len(sys.argv) > 1 else "data.json"
    auto_cleanup()
    run_picker(target_json)
