import os
import json
import re
import time
import shutil
import gc
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from icrawler.builtin import BingImageCrawler
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy import (ImageClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips)

os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
FONT_PATH = r"C:\Windows\Fonts\arialbd.ttf"
PROJECT_ROOT = Path(__file__).parent.absolute()
FETCH_DIR = PROJECT_ROOT / 'images' / 'fetched'
SCENE_DIR = PROJECT_ROOT / 'images' / 'final_scenes'
ARCHIVE_DIR = PROJECT_ROOT / 'archive'
JSON_FILE = "data.json"
RES_W, RES_H = 1080, 1920

def archive_previous_session():
    if FETCH_DIR.exists() and any(FETCH_DIR.iterdir()):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_path = ARCHIVE_DIR / timestamp
        target_path.mkdir(parents=True, exist_ok=True)
        print(f"?? Archiving previous session to: {target_path}")
        for file in FETCH_DIR.glob("*"):
            if file.is_file(): shutil.move(str(file), str(target_path / file.name))
        for sub in FETCH_DIR.glob("scene_*"):
            if sub.is_dir(): shutil.rmtree(sub)

def cleanup(full_wipe=False):
    if full_wipe: archive_previous_session()
    for folder in [SCENE_DIR, PROJECT_ROOT / "temp_audio"]:
        if folder.exists(): shutil.rmtree(folder)
        folder.mkdir(parents=True, exist_ok=True)
    FETCH_DIR.mkdir(parents=True, exist_ok=True)

def fetch_images(scenes):
    print(f"?? Fetching 5 options for each scene...")
    for i, scene in enumerate(scenes):
        scene_dir = FETCH_DIR / f"scene_{i}"
        scene_dir.mkdir(parents=True, exist_ok=True)
        terms = [t.strip() for t in scene.get('search_key', '').split('|')]
        for term in terms:
            crawler = BingImageCrawler(storage={'root_dir': str(scene_dir)})
            crawler.crawl(keyword=term, max_num=5)
            if any(scene_dir.glob("00000*")): break

def render_video(skip_fetch=False):
    # 1. Load Data
    if not os.path.exists(JSON_FILE):
        print(f"? Error: {JSON_FILE} not found."); return
    with open(JSON_FILE, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    scenes = data.get('scenes', [])

    # 2. Fetching Logic
    if not skip_fetch:
        cleanup(full_wipe=True)
        fetch_images(scenes)
        print("\n? Step 1 Complete: 5 options per scene fetched.")
        print("?? NOW RUN: python manual_image_picker.py")
        return 
    
    # 3. Rendering Logic (Only runs with --manual)
    print("?? Starting Render Phase...")
    (PROJECT_ROOT / "temp_audio").mkdir(exist_ok=True)
    (PROJECT_ROOT / "output").mkdir(exist_ok=True)
    
    clips = []
    temp_files = []

    for i, scene in enumerate(scenes):
        img_path = FETCH_DIR / f"{i}.jpg"
        if not img_path.exists():
            print(f"?? Warning: Scene {i} image ({i}.jpg) missing. Skipping."); continue

        print(f"??? Scene {i}: Generating Voiceover...")
        audio_path = PROJECT_ROOT / "temp_audio" / f"scene_{i}.mp3"
        tts = gTTS(text=scene['details'], lang='en')
        tts.save(str(audio_path))
        temp_files.append(audio_path)
        
        # Create Audio/Video Clips
        audio_clip = AudioFileClip(str(audio_path))
        # Add 0.5s silence at end of each scene for natural flow
        duration = audio_clip.duration + 0.5
        
        img_clip = ImageClip(str(img_path)).with_duration(duration)
        
        # Resize to 1080x1920 (Shorts Format)
        img_clip = img_clip.resized(height=RES_H)
        if img_clip.w > RES_W:
            img_clip = img_clip.cropped(x_center=img_clip.w/2, width=RES_W)
        else:
            img_clip = img_clip.resized(width=RES_W)

        img_clip = img_clip.with_audio(audio_clip)
        clips.append(img_clip)

    if not clips:
        print("? No clips created. Did you pick images in Step 2?"); return

    print("?? MoviePy: Assembling and Exporting Final Video...")
    final_video = concatenate_videoclips(clips, method="compose")
    
    output_filename = f"TrendWave_{int(time.time())}.mp4"
    output_path = PROJECT_ROOT / "output" / output_filename
    
    final_video.write_videofile(
        str(output_path), 
        fps=24, 
        codec="libx264", 
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a", 
        remove_temp=True
    )

    print(f"\n? VIDEO CREATED: {output_path}")
    
    # Final Cleanup of scene audio
    for f in temp_files:
        try: os.remove(f)
        except: pass

if __name__ == "__main__":
    import sys
    manual_mode = "--manual" in sys.argv
    render_video(skip_fetch=manual_mode)


