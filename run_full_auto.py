# run_full_auto.py - VERSION 1.2 (ARCHIVING & HYBRID READY)
"""
YouTube Shorts Video Generator
v1.2 (2026-03-16): 
    - Added archive_previous_session() to save old "winner" images.
    - Updated cleanup() to be non-destructive for archiving.
    - Added skip_fetch support for Hybrid workflow (Manual + AI).
"""

import os
import json
import re
import time
import shutil
import gc
import subprocess
import sys
from pathlib import Path
from icrawler.builtin import BingImageCrawler
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from datetime import datetime
from moviepy import (ImageClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips)

# --- SYSTEM CONFIG ---
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
FONT_PATH = r"C:\Windows\Fonts\arialbd.ttf"
PROJECT_ROOT = Path(__file__).parent.absolute()
FETCH_DIR = PROJECT_ROOT / 'images' / 'fetched'
SCENE_DIR = PROJECT_ROOT / 'images' / 'final_scenes'
ARCHIVE_DIR = PROJECT_ROOT / 'archive'
JSON_FILE = "data.json"

RES_W, RES_H = 1080, 1920

def archive_previous_session():
    """Moves existing images from fetched folder to a timestamped archive."""
    if FETCH_DIR.exists() and any(FETCH_DIR.iterdir()):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_path = ARCHIVE_DIR / timestamp
        target_path.mkdir(parents=True, exist_ok=True)
        
        print(f"📦 Archiving previous session images to: {target_path}")
        for file in FETCH_DIR.glob("*"):
            if file.is_file():
                shutil.move(str(file), str(target_path / file.name))

def cleanup(full_wipe=False):
    """Initializes workspace. Archives by default, wipes only if requested."""
    if full_wipe:
        archive_previous_session()
    
    print("🧹 Preparing temp folders...")
    # These folders are always safe to wipe as they are generated per-run
    for folder in [SCENE_DIR, PROJECT_ROOT / "temp_audio"]:
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True, exist_ok=True)
    
    if not FETCH_DIR.exists():
        FETCH_DIR.mkdir(parents=True, exist_ok=True)

def fetch_images(scenes):
    """Uses icrawler to grab images. SKIPPED if manual selection was already done."""
    print(f"🚀 Fetching images for {len(scenes)} scenes...")
    for i, scene in enumerate(scenes):
        # If image already exists (from manual picker), don't overwrite it
        if (FETCH_DIR / f"{i}.jpg").exists():
            print(f"  ⏭️ Image {i}.jpg already exists (Manual Selection), skipping fetch.")
            continue

        search_key = scene.get('search_key', '')
        terms = [t.strip() for t in search_key.split('|')]
        found = False
        for term in terms:
            print(f"  🔍 Trying to fetch image for '{term}'")
            crawler = BingImageCrawler(storage={'root_dir': str(FETCH_DIR)})
            crawler.crawl(keyword=term, max_num=1)
            raw_files = list(FETCH_DIR.glob("00000*"))
            if raw_files:
                process_and_standardize(raw_files[0], i)
                found = True
                print(f"  ✅ Found image for '{term}'")
                break

def process_and_standardize(img_path, index):
    """Crops to 9:16 and resizes."""
    try:
        with Image.open(img_path) as img:
            img = img.convert('RGB')
            target_ratio = RES_W / RES_H
            w, h = img.size
            if (w / h) > target_ratio:
                new_width = int(h * target_ratio)
                left = (w - new_width) // 2
                img = img.crop((left, 0, left + new_width, h))
            else:
                new_height = int(w / target_ratio)
                top = (h - new_height) // 2
                img = img.crop((0, top, w, top + new_height))
            img.resize((RES_W, RES_H), Image.Resampling.LANCZOS).save(FETCH_DIR / f"{index}.jpg", "JPEG", quality=85)
        img_path.unlink()
    except Exception as e:
        print(f"❌ Image process error: {e}")

def create_text_overlay(base_img_path, text, highlight_word_index=None, is_last=False):
    """PIL Based Text Burning (as per your v1.1)"""
    # ... [Keep your existing PIL logic from v1.1 here] ...
    # Ensure it uses the lowercase preference you established
    img = Image.open(base_img_path) if base_img_path and os.path.exists(base_img_path) else Image.new('RGB', (RES_W, RES_H), (25, 25, 25))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 50)
    text = text.lower()
    
    # [Rest of your PIL drawing logic from the prompt goes here]
    # (Abbreviated for brevity, but keep your exact word-highlighting code)
    return img

def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]

def render_video(skip_fetch=False):
    # If we are starting fresh (not skipping fetch), archive the old session
    if not skip_fetch:
        archive_previous_session()
    
    cleanup(full_wipe=False)
    
    if not os.path.exists(JSON_FILE):
        print("❌ Error: data.json missing.")
        return

    with open(JSON_FILE, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)

    scenes_data = data.get('scenes', [])
    
    # Only fetch if we aren't using images from the manual picker
    if not skip_fetch:
        fetch_images(scenes_data)
    
    image_files = {int(p.stem): str(p) for p in FETCH_DIR.glob("*.jpg")}

    video_clips = []
    audio_clips = []

    # --- REST OF RENDERING LOGIC ---
    # [Keep your existing Scene/Sentence/Audio/FFMPEG logic from v1.1 here]
    # ...

if __name__ == "__main__":
    # If "manual" is passed as an argument, it skips fetching to use picker results
    manual_mode = "--manual" in sys.argv
    render_video(skip_fetch=manual_mode)