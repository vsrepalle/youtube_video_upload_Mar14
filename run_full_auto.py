import os
import json
import time
import shutil
import gc
import subprocess
from pathlib import Path
from icrawler.builtin import BingImageCrawler
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy import (ImageClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips)

# --- SYSTEM CONFIG ---
# Ensure these paths are correct for your local machine
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
FONT_PATH = r"C:\Windows\Fonts\arialbd.ttf"
PROJECT_ROOT = Path(__file__).parent.absolute()
FETCH_DIR = PROJECT_ROOT / 'images' / 'fetched'
SCENE_DIR = PROJECT_ROOT / 'images' / 'final_scenes'
JSON_FILE = "data.json"

# Resolution downgrade to 720p for maximum stability on Windows/Python 3.13
RES_W, RES_H = 720, 1280 

def cleanup():
    """Initializes workspace and clears old assets."""
    print("🧹 Cleaning workspace...")
    for folder in [FETCH_DIR, SCENE_DIR, PROJECT_ROOT / "temp_audio"]:
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True, exist_ok=True)

def fetch_images(search_keys):
    """Uses icrawler to grab images from Bing."""
    print(f"🚀 Fetching {len(search_keys)} images...")
    for i, term in enumerate(search_keys):
        crawler = BingImageCrawler(storage={'root_dir': str(FETCH_DIR)})
        crawler.crawl(keyword=term, max_num=1)
        raw_files = list(FETCH_DIR.glob("00000*"))
        if raw_files:
            process_and_standardize(raw_files[0], i)

def process_and_standardize(img_path, index):
    """Crops to 9:16 and resizes to 720p."""
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

def create_text_overlay(base_img_path, text, is_last=False):
    """Draws lowercase text directly onto the image using PIL to bypass MoviePy RAM issues."""
    img = Image.open(base_img_path) if base_img_path and os.path.exists(base_img_path) else Image.new('RGB', (RES_W, RES_H), (25, 25, 25))
    draw = ImageDraw.Draw(img)
    
    # Text settings - using lowercase as requested
    font = ImageFont.truetype(FONT_PATH, 40)
    text = text.lower()
    
    # Word wrap logic
    margin = 60
    max_width = RES_W - (margin * 2)
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and draw.textbbox((0, 0), line + words[0], font=font)[2] < max_width:
            line += words.pop(0) + ' '
        lines.append(line.strip())

    # Draw news text (Center-aligned)
    y_offset = (RES_H - (len(lines) * 55)) // 2
    for line in lines:
        w = draw.textbbox((0, 0), line, font=font)[2]
        # Text with black stroke for readability
        pos = ((RES_W - w) // 2, y_offset)
        draw.text(pos, line, font=font, fill="white", stroke_width=2, stroke_fill="black")
        y_offset += 55

    # Draw Hook/CTA if it's the last scene
    if is_last:
        cta_text = "tune with us for more!".lower()
        cta_font = ImageFont.truetype(FONT_PATH, 50)
        w = draw.textbbox((0, 0), cta_text, font=cta_font)[2]
        draw.text(((RES_W - w) // 2, RES_H - 250), cta_text, font=cta_font, fill="yellow", stroke_width=2, stroke_fill="black")

    return img

def render_video():
    cleanup()
    if not os.path.exists(JSON_FILE):
        print("❌ Error: data.json missing.")
        return

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fetch_images(data.get("metadata", {}).get("image_search_keys", []))
    scenes_data = data.get('scenes', [])
    image_files = {int(p.stem): str(p) for p in FETCH_DIR.glob("*.jpg")}
    
    video_clips = []
    audio_clips = []

    # --- PHASE 1: FLATTENING SCENES ---
    for i, scene in enumerate(scenes_data):
        print(f"🎬 Flattening Scene {i+1}/{len(scenes_data)}")
        text = scene.get('details', '')
        
        # Burn text to image using PIL
        base_img = image_files.get(i)
        final_scene_img = create_text_overlay(base_img, text, is_last=(i == len(scenes_data)-1))
        scene_img_path = SCENE_DIR / f"scene_{i}.jpg"
        final_scene_img.save(scene_img_path)
        
        # Generate Audio
        audio_path = PROJECT_ROOT / "temp_audio" / f"{i}.mp3"
        gTTS(text=text.lower(), lang='en').save(str(audio_path))
        a_clip = AudioFileClip(str(audio_path), buffersize=10000)
        
        # Create lightweight ImageClip
        v_clip = ImageClip(str(scene_img_path)).with_duration(a_clip.duration + 0.3)
        
        video_clips.append(v_clip)
        audio_clips.append(a_clip)
        gc.collect()

    print("\n🚀 Exporting Video and Audio chunks...")
    if not video_clips:
        print("❌ Error: No clips generated.")
        return

    # Use correct concatenation functions for each type
    final_v = concatenate_videoclips(video_clips, method="compose")
    final_a = concatenate_audioclips(audio_clips)
    
    temp_v = PROJECT_ROOT / "temp_v.mp4"
    temp_a = PROJECT_ROOT / "temp_a.mp3"
    out_dir = PROJECT_ROOT / "output"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"TrendWave_{int(time.time())}.mp4"

    # Export separately to avoid memory/pipe errors on Windows
    final_v.write_videofile(str(temp_v), fps=24, audio=False, codec="libx264", preset="ultrafast", threads=1)
    final_a.write_audiofile(str(temp_a))

    final_v.close()
    final_a.close()

    # --- PHASE 2: FINAL STITCHING ---
    print("🔗 Final Stitching with FFMPEG...")
    try:
        subprocess.run([
            'ffmpeg', '-y', '-i', str(temp_v), '-i', str(temp_a), 
            '-c:v', 'copy', '-c:a', 'aac', '-shortest', str(out_file)
        ], check=True)
        print(f"\n✅ Video Successfully Rendered: {out_file}")
    except Exception as e:
        print(f"❌ Final stitch failed: {e}")
    
    # Cleanup temp files
    for f in [temp_v, temp_a]: 
        if f.exists(): f.unlink()

if __name__ == "__main__":
    render_video()