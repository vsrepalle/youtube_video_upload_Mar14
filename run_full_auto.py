# run_full_auto.py - VERSION 1.1 (SENTENCE-BY-SENTENCE WITH WORD HIGHLIGHTING)
"""
YouTube Shorts Video Generator - PIL-based text burning approach
ENHANCED VERSION: Sentence-by-sentence display with word highlighting

VERSION HISTORY:
v1.1 (2026-03-14): Sentence-by-sentence subtitles with word highlighting
    - Splits scenes into sentences for better pacing
    - Highlights spoken words in yellow as they are spoken
    - Moves subtitles to bottom of video to avoid face overlay
    - Creates multiple frames per sentence for smooth highlighting

v1.0 (2026-03-14): Initial stable version with PIL text overlay
    - Burns text directly onto images using PIL
    - Creates video clips with static text
    - Uses FFMPEG for final stitching
    - No dynamic subtitles or word highlighting

v0.9 (2026-03-14): Attempted dynamic subtitle system (REVERTED)
    - Tried to use app/video system with dynamic subtitles
    - Failed due to import issues and ImageProcessor errors
    - REVERTED BACK TO v1.0 for stability
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
from moviepy import (ImageClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips)

# --- SYSTEM CONFIG ---
# Ensure these paths are correct for your local machine
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
FONT_PATH = r"C:\Windows\Fonts\arialbd.ttf"
PROJECT_ROOT = Path(__file__).parent.absolute()
FETCH_DIR = PROJECT_ROOT / 'images' / 'fetched'
SCENE_DIR = PROJECT_ROOT / 'images' / 'final_scenes'
JSON_FILE = "data.json"

# Resolution for YouTube Shorts (9:16 aspect ratio)
RES_W, RES_H = 1080, 1920

def cleanup():
    """Initializes workspace and clears old assets."""
    print("🧹 Cleaning workspace...")
    for folder in [FETCH_DIR, SCENE_DIR, PROJECT_ROOT / "temp_audio"]:
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True, exist_ok=True)

def fetch_images(scenes):
    """Uses icrawler to grab images from Bing with fallback search terms."""
    print(f"🚀 Fetching images for {len(scenes)} scenes...")
    for i, scene in enumerate(scenes):
        search_key = scene.get('search_key', '')
        if not search_key:
            print(f"⚠️ No search_key for scene {i}, skipping")
            continue

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
        if not found:
            print(f"  ❌ No images found for scene {i} with any term")

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

def create_text_overlay(base_img_path, text, highlight_word_index=None, is_last=False):
    """Draws lowercase text directly onto the image using PIL to bypass MoviePy RAM issues."""
    img = Image.open(base_img_path) if base_img_path and os.path.exists(base_img_path) else Image.new('RGB', (RES_W, RES_H), (25, 25, 25))
    draw = ImageDraw.Draw(img)

    # Text settings - using lowercase as requested
    font = ImageFont.truetype(FONT_PATH, 50)  # Increased font size for better visibility
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

    # Draw text at BOTTOM of image (lower position to avoid faces)
    y_offset = RES_H - 120 - (len(lines) * 60)  # Lower position and increased line spacing
    for line_idx, line in enumerate(lines):
        line_words = line.split()
        x_offset = margin

        for word_idx, word in enumerate(line_words):
            # Check if this word should be highlighted
            global_word_index = sum(len(lines[j].split()) for j in range(line_idx)) + word_idx
            is_highlighted = (highlight_word_index is not None and global_word_index == highlight_word_index)

            # Word with space
            word_with_space = word + ' '

            # Get word dimensions
            bbox = draw.textbbox((0, 0), word_with_space, font=font)
            word_width = bbox[2] - bbox[0]

            # Highlight current word in red if it's being spoken
            if is_highlighted:
                draw.text((x_offset, y_offset), word_with_space, font=font, fill="red", stroke_width=2, stroke_fill="black")
            else:
                # Normal word in white with black stroke
                draw.text((x_offset, y_offset), word_with_space, font=font, fill="white", stroke_width=2, stroke_fill="black")

            x_offset += word_width

        y_offset += 60  # Increased line spacing

    # Draw Hook/CTA if it's the last scene
    if is_last:
        cta_text = "tune with us for more!".lower()
        cta_font = ImageFont.truetype(FONT_PATH, 60)  # Larger CTA font
        w = draw.textbbox((0, 0), cta_text, font=cta_font)[2]
        draw.text(((RES_W - w) // 2, RES_H - 80), cta_text, font=cta_font, fill="yellow", stroke_width=2, stroke_fill="black")

    return img

def split_into_sentences(text):
    """Split text into sentences using basic punctuation."""
    import re
    # Split on period, question mark, or exclamation mark followed by space or end
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    # Filter out empty sentences
    return [s.strip() for s in sentences if s.strip()]

def render_video():
    cleanup()
    if not os.path.exists(JSON_FILE):
        print("❌ Error: data.json missing.")
        return

    with open(JSON_FILE, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)

    scenes_data = data.get('scenes', [])
    fetch_images(scenes_data)
    image_files = {int(p.stem): str(p) for p in FETCH_DIR.glob("*.jpg")}

    video_clips = []
    audio_clips = []

    # --- PHASE 1: FLATTENING SCENES ---
    for i, scene in enumerate(scenes_data):
        print(f"🎬 Processing Scene {i+1}/{len(scenes_data)}")
        full_text = scene.get('details', '')

        # Split scene into sentences for sentence-by-sentence display
        sentences = split_into_sentences(full_text)
        if not sentences:
            sentences = [full_text]  # Fallback if no sentences found

        base_img = image_files.get(i)
        scene_video_clips = []
        scene_audio_clips = []

        for sentence_idx, sentence in enumerate(sentences):
            print(f"  📝 Processing sentence {sentence_idx+1}/{len(sentences)}: {sentence[:50]}...")

            # Generate audio for this sentence
            audio_path = PROJECT_ROOT / "temp_audio" / f"{i}_{sentence_idx}.mp3"
            gTTS(text=sentence.lower(), lang='en').save(str(audio_path))
            sentence_audio = AudioFileClip(str(audio_path), buffersize=10000)

            # Estimate timing for word highlighting
            words = sentence.split()
            if not words:
                continue

            # Rough estimate: 0.3 seconds per word for highlighting timing
            word_duration = max(0.3, sentence_audio.duration / len(words))

            # Create video frames for this sentence with word highlighting
            sentence_frames = []
            current_time = 0

            for word_idx in range(len(words)):
                # Create image with current word highlighted
                highlighted_img = create_text_overlay(
                    base_img,
                    sentence,
                    highlight_word_index=word_idx,
                    is_last=(i == len(scenes_data)-1 and sentence_idx == len(sentences)-1)
                )

                # Save frame
                frame_path = SCENE_DIR / f"scene_{i}_sentence_{sentence_idx}_word_{word_idx}.jpg"
                highlighted_img.save(frame_path)
                sentence_frames.append(str(frame_path))

                current_time += word_duration

            # Create video clip from frames for this sentence
            if sentence_frames:
                # Create ImageClips for each frame with appropriate duration
                frame_clips = []
                for frame_idx, frame_path in enumerate(sentence_frames):
                    duration = word_duration if frame_idx < len(sentence_frames) - 1 else sentence_audio.duration - (frame_idx * word_duration)
                    duration = max(0.1, duration)  # Minimum duration
                    frame_clip = ImageClip(frame_path).with_duration(duration)
                    frame_clips.append(frame_clip)

                sentence_video = concatenate_videoclips(frame_clips, method="compose")
                scene_video_clips.append(sentence_video)
                scene_audio_clips.append(sentence_audio)

        # Concatenate all sentences for this scene
        if scene_video_clips:
            scene_video = concatenate_videoclips(scene_video_clips, method="compose")
            scene_audio = concatenate_audioclips(scene_audio_clips)

            video_clips.append(scene_video)
            audio_clips.append(scene_audio)

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
