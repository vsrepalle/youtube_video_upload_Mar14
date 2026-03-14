# app/main.py - VERSION 1.0 (STABLE)
"""
Alternative video composer with modular architecture
STABLE VERSION: Basic composition without speed features

VERSION HISTORY:
v1.0 (2026-03-14): Stable modular video composer
    - Basic video composition with fixed timing
    - Modular audio, image, text components
    - No speed adjustment features

v0.9 (2026-03-14): Attempted speed features (REVERTED)
    - Added speed parameters to composition
    - Tried dynamic speed adjustments
    - REVERTED due to synchronization issues
"""

from moviepy import CompositeVideoClip, concatenate_videoclips
import config
from pathlib import Path
import time
import gc
import sys
import os

# Fix for relative imports when running directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Try relative imports first
    from .audio import load_audio, estimate_duration_from_text
    from .images import ImageProcessor
    from .text import text_generator
    from .compositor import VideoCompositor as _VideoCompositor
    from .renderer import Renderer
    from .utils import timeit, log_memory, Timer, ensure_dir
except ImportError:
    # Fall back to absolute imports
    from audio import load_audio, estimate_duration_from_text
    from images import ImageProcessor
    from text import text_generator
    from compositor import VideoCompositor as _VideoCompositor
    from renderer import Renderer
    from utils import timeit, log_memory, Timer, ensure_dir

class VideoComposer:
    def __init__(self):
        self.width = config.VIDEO_WIDTH
        self.height = config.VIDEO_HEIGHT
        self.fps = config.FPS
        self.start_time = None
        self.split_screen_enabled = getattr(config, 'SPLIT_SCREEN_ENABLED', True)
        
        self.image_processor = ImageProcessor(self.width, self.height)
        self.compositor = _VideoCompositor(self.width, self.height)
        self.renderer = Renderer(self.fps)
        
    def _log_timing(self, stage: str):
        current_time = time.time()
        if self.start_time is None:
            self.start_time = current_time
            print(f"\n🕒 Started at: {time.strftime('%H:%M:%S')}")
        else:
            elapsed = current_time - self.start_time
            stage_time = current_time - self.last_time if hasattr(self, 'last_time') else 0
            print(f"  └─ {stage}: {stage_time:.1f}s (total: {elapsed:.1f}s)")
        self.last_time = current_time
    
    @timeit
    @log_memory
    def compose(self, images: list[Path], audio_path: str, english_text: str,
                headline: str, hook: str, subscribe_hook: str,
                output_path: str = "output/final_short.mp4") -> str:
        
        print("\n" + "="*70)
        print("🎬 VIDEO COMPOSER")
        if self.split_screen_enabled:
            print("📱 MODE: SPLIT SCREEN (images shown in pairs)")
        else:
            print("📱 MODE: SINGLE IMAGE")
        print("="*70)
        
        self.start_time = time.time()
        self._log_timing("start")
        
        output_dir = Path(output_path).parent
        ensure_dir(output_dir)
        
        text_generator.clear_cache()
        gc.collect()
        self._log_timing("cache cleanup")
        
        # 1. Load audio
        audio = None
        duration = 30  # Default duration
        if audio_path and Path(audio_path).exists():
            audio, duration = load_audio(audio_path)
        if not audio:
            duration = estimate_duration_from_text(english_text)
        self._log_timing("audio loaded")
        
        # 2. Process images (with split screen if enabled)
        if not images:
            print("\n[IMAGES] No images provided - using gradient background")
            clips = [self.image_processor.create_gradient_background(
                self.width, self.height, duration
            )]
        elif self.split_screen_enabled and len(images) >= 2:
            num_screens = (len(images) + 1) // 2
            dur_per_screen = duration / num_screens
            print(f"\n[SPLIT SCREEN] Creating {num_screens} split screens from {len(images)} images")
            clips = self.image_processor.process_batch(images, dur_per_screen)
        else:
            num_images = max(1, len(images))
            dur_per_image = duration / num_images
            print(f"\n[SINGLE IMAGE] Processing {num_images} images")
            clips = self.image_processor.process_batch(images, dur_per_image)
        
        self._log_timing("images processed")
        
        # Create slideshow
        if len(clips) == 1:
            slideshow = clips[0]
        else:
            slideshow = concatenate_videoclips(clips, method="compose")
        self._log_timing("slideshow created")
        
        # 3. Create text elements
        print(f"\n[TEXT] Creating text elements...")
        header = self.compositor.create_header(headline, duration)
        subtitle_clips = self.compositor.create_subtitles(english_text, duration)
        hook_clip = self.compositor.create_hook(hook, duration)
        overlay, end_text = self.compositor.create_end_screen(subscribe_hook, duration)
        self._log_timing("text elements created")
        
        # 4. Compose final video
        print(f"\n[COMPOSE] Building final video...")
        layers = [slideshow, header]
        layers.extend(subtitle_clips)
        layers.extend([hook_clip, overlay, end_text])
        
        final_video = CompositeVideoClip(layers, size=(self.width, self.height))
        final_video = final_video.set_duration(duration)
        
        if audio:
            final_video = final_video.set_audio(audio)
        self._log_timing("composition ready")
        
        # 5. Render
        print(f"\n[RENDER] Starting render...")
        render_time, file_size = self.renderer.render(final_video, output_path, duration)
        self._log_timing("rendering complete")
        
        # 6. Cleanup
        final_video.close()
        if audio:
            audio.close()
        text_generator.clear_cache()
        gc.collect()
        
        total_time = time.time() - self.start_time
        
        # Print summary
        print("\n" + "="*70)
        print("📊 PERFORMANCE SUMMARY")
        print("="*70)
        print(f"Mode:               {'Split Screen' if self.split_screen_enabled else 'Single Image'}")
        print(f"Started:            {time.strftime('%H:%M:%S', time.localtime(self.start_time))}")
        print(f"Completed:          {time.strftime('%H:%M:%S')}")
        print(f"Total time:         {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
        print(f"Video duration:     {duration:.1f} seconds")
        print(f"Images processed:   {len(images)}")
        print(f"Clips created:      {len(clips)}")
        print(f"Render speed:       {duration/render_time:.1f}x realtime")
        print(f"File size:          {file_size/1024/1024:.1f} MB")
        print("="*70)
        print(f"✅ Output: {output_path}")
        print("="*70)
        
        return output_path

# Create the instance and export function
_composer_instance = None

def get_composer():
    """Get or create VideoComposer instance"""
    global _composer_instance
    if _composer_instance is None:
        _composer_instance = VideoComposer()
    return _composer_instance

def make_short_video(images, audio_path, english_text, headline, hook, subscribe_hook, output_path="output/final_short.mp4"):
    """Convenience function to create a video"""
    composer = get_composer()
    return composer.compose(
        images=images,
        audio_path=audio_path,
        english_text=english_text,
        headline=headline,
        hook=hook,
        subscribe_hook=subscribe_hook,
        output_path=output_path
    )

# Explicitly export the function
__all__ = ['make_short_video', 'VideoComposer']

# Command line handling
if __name__ == "__main__":
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description='Generate video from JSON data')
    parser.add_argument('--json', required=True, help='Path to JSON data file')
    parser.add_argument('--audio', help='Path to audio file')
    parser.add_argument('--output', help='Output path')
    args = parser.parse_args()
    
    # Load JSON data
    with open(args.json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Set output path
    output_path = args.output if args.output else f"output/{data['headline'][:30]}.mp4"
    
    # Generate video
    make_short_video(
        images=[],  # Add your image fetching logic here
        audio_path=args.audio,
        english_text=data['details'],
        headline=data['headline'],
        hook=data['hook_text'],
        subscribe_hook=data['subscribe_hook'],
        output_path=output_path
    )