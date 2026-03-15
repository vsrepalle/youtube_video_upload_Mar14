# app/video/main_video.py - VERSION 1.0 (STABLE)
"""
Main video composition module with audio-video synchronization
STABLE VERSION: Basic video creation without speed adjustments

VERSION HISTORY:
v1.0 (2026-03-14): Stable video composition system
    - Basic video creation with fixed timing
    - Audio-video synchronization
    - No speed adjustment features

v0.9 (2026-03-14): Attempted speed adjustments (REVERTED)
    - Added speed parameter to create_video
    - Tried to adjust video speed dynamically
    - REVERTED due to synchronization issues
"""

import sys
import os
from pathlib import Path
import time
import gc
import traceback
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import moviepy config first
try:
    import moviepy_config
except:
    pass

try:
    import config
    from .audio import load_audio, estimate_duration_from_text
    from .images_root import ImageProcessor
    from .compositor import VideoCompositor
    from .renderer import Renderer
    from moviepy import CompositeVideoClip, concatenate_videoclips, ColorClip, TextClip
    
    # Test if TextClip works with ImageMagick
    try:
        test_txt = TextClip("Test", fontsize=10, color='white', font='Arial', duration=0.1)
        TEXT_WORKS = True
    except:
        TEXT_WORKS = False
        print("⚠️ TextClip not available - using fallback")
    
    # Get image display duration from config
    try:
        IMAGE_DISPLAY_DURATION = getattr(config, 'IMAGE_DISPLAY_DURATION', 3.5)
    except:
        IMAGE_DISPLAY_DURATION = 3.5
    
    FULL_MODE = True
    print("✅ Modules loaded")
    print(f"   📸 Base image duration: {IMAGE_DISPLAY_DURATION}s")
except Exception as e:
    print(f"⚠️ Limited mode: {e}")
    FULL_MODE = False
    IMAGE_DISPLAY_DURATION = 3.5

class VideoComposer:
    def __init__(self):
        if FULL_MODE:
            self.width = config.VIDEO_WIDTH
            self.height = config.VIDEO_HEIGHT
            self.fps = config.FPS
            self.image_processor = ImageProcessor(self.width, self.height)
            self.compositor = VideoCompositor(self.width, self.height) if TEXT_WORKS else None
            self.renderer = Renderer(self.fps)
            print(f"✅ Composer ready: {self.width}x{self.height}")
        else:
            self.width = 1080
            self.height = 1920
            self.fps = 30
            self.image_processor = ImageProcessor(self.width, self.height)
            self.compositor = None
            self.renderer = Renderer(self.fps)
    
    def _log_timing(self, stage, start_time=None):
        """Simple timing logger"""
        current = time.time()
        if not hasattr(self, 'start_time'):
            self.start_time = current
        if start_time:
            print(f"   ⏱️ {stage}: {current - start_time:.2f}s")
    
    def compose(self, images, audio_path, english_text, headline, hook, subscribe_hook, output_path):
        print("\n" + "="*70)
        print("🎬 STARTING VIDEO CREATION")
        print("="*70)
        
        print(f"📸 Images available: {len(images)}")
        print(f"🔊 Audio: {audio_path}")
        print(f"📰 Headline: {headline[:50]}...")
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # 1. LOAD AUDIO - Get exact duration
            audio = None
            duration = 30
            if audio_path and Path(audio_path).exists():
                audio, duration = load_audio(audio_path)
                print(f"✅ Audio loaded: {duration:.2f}s")
            else:
                duration = estimate_duration_from_text(english_text)
                print(f"📝 Using text duration: {duration:.2f}s")
            
            # 2. PROCESS IMAGES WITH SMART LOOPING - NO BLACK SCREENS!
            images_start = time.time()
            print(f"\n📸 [IMAGE LOOPING ENGINE]")
            print(f"   ⏱️ Need to fill: {duration:.2f}s")
            
            if not images:
                print("   ⚠️ No images - using gradient background")
                clips = [self.image_processor.create_gradient_background(self.width, self.height, duration)]
            else:
                # Use the smart looping method that guarantees full duration
                clips = self.image_processor.process_batch_with_loop(
                    image_paths=images,
                    target_duration=duration,
                    base_duration=IMAGE_DISPLAY_DURATION
                )
            
            self._log_timing("Image processing", images_start)
            
            # 3. CREATE SLIDESHOW
            slideshow_start = time.time()
            print(f"\n🎞️ Creating slideshow from {len(clips)} clips...")
            
            if len(clips) == 1:
                slideshow = clips[0]
            else:
                slideshow = concatenate_videoclips(clips, method="compose")
            
            self._log_timing("Slideshow creation", slideshow_start)
            
            # 4. ADD TEXT ELEMENTS
            text_start = time.time()
            print(f"\n📝 Adding text elements...")
            layers = [slideshow]
            
            if self.compositor:
                header = self.compositor.create_header(headline, duration)
                if header:
                    layers.append(header)
                    print("   ✅ Header added")
                
                subtitles = self.compositor.create_subtitles(english_text, duration)
                if subtitles:
                    layers.extend(subtitles)
                    print(f"   ✅ {len(subtitles)} subtitle clips added")
                
                hook_clip = self.compositor.create_hook(hook, duration)
                if hook_clip:
                    layers.append(hook_clip)
                    print("   ✅ Hook added")
                
                overlay, end_text = self.compositor.create_end_screen(subscribe_hook, duration)
                if overlay:
                    layers.append(overlay)
                    print("   ✅ Overlay added")
                if end_text:
                    layers.append(end_text)
                    print("   ✅ End text added")
            else:
                # Simple colored bar as header (fallback)
                header_bg = ColorClip(size=(self.width, 80), color=(0,0,0)).set_opacity(0.7).set_duration(duration)
                layers.append(header_bg.with_position("top"))
                print("   ✅ Fallback header added")
            
            self._log_timing("Text creation", text_start)
            
            # 5. COMPOSE FINAL VIDEO
            compose_start = time.time()
            print(f"\n🎥 Building final video with {len(layers)} layers...")
            
            final = CompositeVideoClip([c for c in layers if c], size=(self.width, self.height))
            final = final.set_duration(duration)
            
            if audio:
                final = final.set_audio(audio)
            
            self._log_timing("Composition", compose_start)
            
            # 6. RENDER
            render_start = time.time()
            print(f"\n⚡ Rendering to {output_path}...")
            render_time, file_size = self.renderer.render(final, output_path, duration)
            
            # 7. FINAL REPORT
            print("\n" + "="*70)
            print("✅ VIDEO CREATED SUCCESSFULLY!")
            print("="*70)
            print(f"📁 Output: {output_path}")
            print(f"📏 Size: {file_size:.1f} MB")
            print(f"⏱️ Duration: {duration:.2f}s")
            print(f"📸 Images used: {len(images)} original, looped to fill full duration")
            print(f"🎯 No black screens - images play throughout")
            print("="*70)
            
            return output_path
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            traceback.print_exc()
            
            # Ultra simple fallback
            print("\n⚠️ Creating minimal fallback video...")
            try:
                bg = ColorClip(size=(self.width, self.height), color=(45,45,100), duration=10)
                bg.write_videofile(output_path, fps=24, codec='libx264', preset='ultrafast')
                print(f"✅ Fallback video created: {output_path}")
            except Exception as e2:
                print(f"❌ Fallback also failed: {e2}")
            
            return output_path

def make_short_video(images, audio_path, english_text, headline, hook, subscribe_hook, output_path):
    """Main entry point for video creation"""
    print("\n🎬 [API] make_short_video called")
    composer = VideoComposer()
    return composer.compose(images, audio_path, english_text, headline, hook, subscribe_hook, output_path)