# app/video/images_root.py - COMPLETE WITH LOOPING SUPPORT
"""
Image processing module - Single images only with looping to fill duration
Automatically repeats images to ensure no black screen
"""

from moviepy.editor import ImageClip, ColorClip, CompositeVideoClip
from pathlib import Path
import time
import traceback

try:
    import config
    CONFIG_AVAILABLE = True
except:
    CONFIG_AVAILABLE = False

class ImageProcessor:
    def __init__(self, width=1080, height=1920):
        self.width = width
        self.height = height
        
        # Load settings from config
        if CONFIG_AVAILABLE:
            self.image_settings = config.get_image_settings() if hasattr(config, 'get_image_settings') else {}
            self.fit_mode = self.image_settings.get("fit_mode", "cover") if isinstance(self.image_settings, dict) else "cover"
            self.transition_enabled = getattr(config, 'TRANSITION_ENABLED', True)
            self.transition_duration = getattr(config, 'TRANSITION_DURATION', 0.5)
        else:
            self.fit_mode = "cover"
            self.transition_enabled = True
            self.transition_duration = 0.5
        
        print(f"\n🖼️ ImageProcessor initialized: {width}x{height}")
        print(f"   📐 Fit mode: {self.fit_mode}")
        print(f"   🔄 Transitions: {'ON' if self.transition_enabled else 'OFF'} ({self.transition_duration}s)")
        print(f"   📸 Mode: Single images with auto-looping")

    def fit_image_to_frame(self, clip):
        """Fit image to frame based on fit_mode setting"""
        if self.fit_mode == "cover":
            # Fill entire frame (may crop) - BEST for full screen
            if clip.w / clip.h > self.width / self.height:
                # Image wider - fit to height
                clip = clip.resize(height=self.height)
                # Center crop width
                if clip.w > self.width:
                    clip = clip.crop(x_center=clip.w/2, width=self.width)
            else:
                # Image taller - fit to width
                clip = clip.resize(width=self.width)
                # Center crop height
                if clip.h > self.height:
                    clip = clip.crop(y_center=clip.h/2, height=self.height)
        
        elif self.fit_mode == "contain":
            # Show entire image (adds black bars)
            if clip.w / clip.h > self.width / self.height:
                # Image wider - fit to width
                clip = clip.resize(width=self.width)
                # Add black bars top/bottom
                clip = clip.on_color(size=(self.width, self.height), 
                                    color=(0,0,0), pos=('center', 'center'))
            else:
                # Image taller - fit to height
                clip = clip.resize(height=self.height)
                # Add black bars left/right
                clip = clip.on_color(size=(self.width, self.height), 
                                    color=(0,0,0), pos=('center', 'center'))
        
        return clip

    def process_single(self, img_path: Path, duration: float):
        """
        Process a single image - fit to frame
        No zoom, no split - just clean image display
        """
        try:
            if not img_path.exists():
                print(f"   ⚠️ Image not found: {img_path}")
                return ColorClip((self.width, self.height), color=(30,30,60)).set_duration(duration)
            
            # Load image
            clip = ImageClip(str(img_path)).set_duration(duration)
            
            # Fit to frame
            clip = self.fit_image_to_frame(clip)
            
            print(f"   ✅ Processed: {img_path.name}")
            return clip
            
        except Exception as e:
            print(f"   ❌ Failed to process {img_path.name}: {e}")
            traceback.print_exc()
            return ColorClip((self.width, self.height), color=(30,30,60)).set_duration(duration)

    def process_batch_with_loop(self, image_paths: list[Path], target_duration: float, base_duration: float = 3.5):
        """
        Process images with automatic looping to fill exact target duration
        This is the SMART method that ensures no black screen
        
        Args:
            image_paths: List of original images
            target_duration: Total video duration in seconds
            base_duration: Desired duration per image segment
        
        Returns:
            List of clips that exactly fill target_duration
        """
        print(f"\n🔄 IMAGE LOOPING ENGINE")
        print(f"   📊 Original images: {len(image_paths)}")
        print(f"   ⏱️ Target duration: {target_duration:.2f}s")
        print(f"   ⏱️ Base segment duration: {base_duration:.2f}s")
        
        if not image_paths:
            print("   ⚠️ No images provided")
            return []
        
        num_original = len(image_paths)
        
        # Calculate how many segments we need to fill the duration
        # We want each segment to be approximately base_duration seconds
        segments_needed = int(target_duration / base_duration) + 1
        
        # Create repeated list by cycling through original images
        repeated_images = []
        for i in range(segments_needed):
            repeated_images.append(image_paths[i % num_original])
        
        # Calculate exact duration per segment to perfectly match video length
        exact_duration = target_duration / segments_needed
        
        print(f"   🔁 Creating {segments_needed} segments")
        if segments_needed > num_original:
            print(f"   🔄 Each image will repeat {segments_needed // num_original} times")
            if segments_needed % num_original != 0:
                print(f"   🔄 Last cycle will use {segments_needed % num_original} images")
        else:
            print(f"   📸 Using first {segments_needed} images (no looping needed)")
        
        print(f"   ⏱️ Each segment: {exact_duration:.3f}s")
        print(f"   ✅ Total: {exact_duration * segments_needed:.3f}s = Video duration")
        print(f"   🎯 NO BLACK SCREEN - Images fill entire video")
        
        # Process the repeated images
        clips = []
        for i, img_path in enumerate(repeated_images):
            print(f"\n   Segment {i+1}/{segments_needed}: {img_path.name}")
            clip = self.process_single(img_path, exact_duration)
            
            # Add crossfade transition between clips if enabled
            if self.transition_enabled and i > 0:
                clip = clip.crossfadein(self.transition_duration)
            
            clips.append(clip)
        
        print(f"\n✅ Created {len(clips)} clips totaling {target_duration:.2f}s")
        return clips

    def process_batch(self, image_paths: list[Path], duration_per_image: float):
        """
        Legacy method - processes images without looping
        Kept for backward compatibility
        """
        print(f"\n📸 Processing {len(image_paths)} images at {duration_per_image:.2f}s each")
        clips = []
        for i, img_path in enumerate(image_paths):
            clip = self.process_single(img_path, duration_per_image)
            if self.transition_enabled and i > 0:
                clip = clip.crossfadein(self.transition_duration)
            clips.append(clip)
        return clips

    def create_gradient_background(self, width, height, duration):
        """Create gradient background as fallback when no images available"""
        print(f"   🎨 Creating gradient background: {width}x{height}, {duration:.2f}s")
        return ColorClip((width, height), color=(15,15,35)).set_duration(duration)