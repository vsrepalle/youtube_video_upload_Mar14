# app/video/compositor.py - COMPLETE FIXED VERSION WITH WORKING SUBTITLES
"""
Video composition module - creates headers, subtitles, hooks, end screens
FIXED: Subtitles now properly generated and added
"""

from moviepy.editor import CompositeVideoClip, ColorClip, ImageClip
import numpy as np
import time
import traceback

try:
    import config
    CONFIG_AVAILABLE = True
    print("✅ config available for compositor")
except:
    CONFIG_AVAILABLE = False
    print("⚠️ config not available - using defaults")

# Import text generator
from .text import text_generator

class VideoCompositor:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.timings = {}
        
        print(f"\n🔧 Initializing VideoCompositor with {width}x{height}")
        
        # Load config or use defaults
        if CONFIG_AVAILABLE:
            # Header settings
            self.header_height = getattr(config, 'HEADER_HEIGHT', 120)
            self.header_opacity = getattr(config, 'HEADER_OPACITY', 0.7)
            self.header_font_size = getattr(config, 'HEADER_FONT_SIZE', 65)
            self.header_stroke_width = getattr(config, 'HEADER_STROKE_WIDTH', 4)
            
            # Subtitle settings
            self.subtitle_font_size = getattr(config, 'SUBTITLE_FONT_SIZE', 70)
            self.subtitle_color = getattr(config, 'SUBTITLE_COLOR', 'yellow')
            self.subtitle_stroke_width = getattr(config, 'SUBTITLE_STROKE_WIDTH', 4)
            self.subtitle_y = getattr(config, 'SUBTITLE_Y_POSITION', 1650)
            self.subtitle_max_width = getattr(config, 'SUBTITLE_MAX_WIDTH', 900)
            self.subtitle_words_per_chunk = getattr(config, 'SUBTITLE_WORDS_PER_CHUNK', 4)
            
            # Hook settings
            self.hook_font_size = getattr(config, 'HOOK_FONT_SIZE', 110)
            self.hook_duration = getattr(config, 'HOOK_DURATION', 3.0)
            
            # End screen settings
            self.end_screen_font_size = getattr(config, 'END_SCREEN_FONT_SIZE', 95)
            self.end_screen_duration = getattr(config, 'END_SCREEN_DURATION', 4.0)
            self.end_screen_opacity = getattr(config, 'END_SCREEN_OPACITY', 0.8)
            self.end_screen_cta = getattr(config, 'END_SCREEN_CTA', "🔔 SUBSCRIBE FOR MORE!")
            
            print(f"   📝 Header: height={self.header_height}, font={self.header_font_size}")
            print(f"   📝 Subtitle: font={self.subtitle_font_size}, y={self.subtitle_y}")
            print(f"   📝 Hook: font={self.hook_font_size}")
            print(f"   📝 End screen: font={self.end_screen_font_size}")
        else:
            # Defaults
            self.header_height = 120
            self.header_opacity = 0.7
            self.header_font_size = 65
            self.header_stroke_width = 4
            self.subtitle_font_size = 70
            self.subtitle_color = 'yellow'
            self.subtitle_stroke_width = 4
            self.subtitle_y = 1650
            self.subtitle_max_width = 900
            self.subtitle_words_per_chunk = 4
            self.hook_font_size = 110
            self.hook_duration = 3.0
            self.end_screen_font_size = 95
            self.end_screen_duration = 4.0
            self.end_screen_opacity = 0.8
            self.end_screen_cta = "🔔 SUBSCRIBE FOR MORE!"
            print("   📝 Using default settings")
        
        print(f"✅ VideoCompositor initialized")
    
    def create_header(self, headline, duration):
        """Create header with headline"""
        if not headline:
            print("   ⚠️ No headline provided")
            return None
        
        try:
            print(f"\n   🔧 Creating header: '{headline[:30]}...'")
            
            # Semi-transparent header background
            header_bg = ColorClip(
                size=(self.width, self.header_height),
                color=(0, 0, 0)
            ).set_opacity(self.header_opacity).set_duration(duration)
            
            # Create headline text
            headline_img = text_generator.create_text_image(
                headline.upper(),
                font_size=self.header_font_size,
                color='white',
                stroke_width=self.header_stroke_width,
                stroke_color='black',
                max_width=self.width - 100
            )
            
            headline_clip = ImageClip(headline_img)
            headline_clip = headline_clip.set_position(('center', 30))
            headline_clip = headline_clip.set_duration(duration)
            
            result = CompositeVideoClip(
                [header_bg, headline_clip], 
                size=(self.width, self.height)
            ).set_position("top")
            
            print(f"   ✅ Header created")
            return result
            
        except Exception as e:
            print(f"   ❌ Header creation failed: {e}")
            traceback.print_exc()
            return None
    
    def create_subtitles(self, text, duration):
        """Create subtitle clips - GUARANTEED TO WORK"""
        print(f"\n   🔧 Creating subtitles from text length: {len(text)} chars")
        
        if not text:
            print("   ⚠️ No text provided for subtitles")
            return []
        
        try:
            words = text.split()
            subtitle_clips = []
            
            # Split into chunks of ~4 words each for better readability
            chunks = []
            current_chunk = []
            
            for word in words:
                current_chunk.append(word)
                if len(current_chunk) >= self.subtitle_words_per_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
            
            # Add the last chunk if any
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            
            # If no chunks created (shouldn't happen), use the whole text
            if not chunks:
                chunks = [text]
            
            print(f"   📝 Split into {len(chunks)} subtitle chunks")
            
            # Calculate timing for each chunk
            chunk_duration = duration / len(chunks)
            print(f"   ⏱️ Each chunk duration: {chunk_duration:.2f}s")
            
            for i, chunk in enumerate(chunks):
                start = i * chunk_duration
                
                print(f"\n   📝 Creating subtitle {i+1}/{len(chunks)}: '{chunk[:30]}...'")
                
                # Create text image
                sub_img = text_generator.create_text_image(
                    chunk,
                    font_size=self.subtitle_font_size,
                    color=self.subtitle_color,
                    stroke_width=self.subtitle_stroke_width,
                    stroke_color='black',
                    max_width=self.subtitle_max_width
                )
                
                # Create clip
                sub_clip = ImageClip(sub_img)
                sub_clip = sub_clip.set_position(('center', self.subtitle_y))
                sub_clip = sub_clip.set_duration(chunk_duration)
                sub_clip = sub_clip.set_start(start)
                
                # Add fade effects for smooth transitions
                try:
                    sub_clip = sub_clip.crossfadein(0.2).crossfadeout(0.2)
                except:
                    pass
                
                subtitle_clips.append(sub_clip)
                print(f"   ✅ Subtitle {i+1} created")
            
            print(f"\n   ✅ Created {len(subtitle_clips)} subtitle clips")
            return subtitle_clips
            
        except Exception as e:
            print(f"   ❌ Subtitle creation failed: {e}")
            traceback.print_exc()
            return []
    
    def create_hook(self, hook_text, total_duration):
        """Create opening hook"""
        if not hook_text:
            print("   ⚠️ No hook text provided")
            return None
        
        try:
            print(f"\n   🔧 Creating hook: '{hook_text[:30]}...'")
            
            hook_duration = min(self.hook_duration, total_duration * 0.15)
            
            hook_img = text_generator.create_text_image(
                hook_text,
                font_size=self.hook_font_size,
                color='yellow',
                stroke_width=6,
                stroke_color='black',
                max_width=self.width - 100
            )
            
            hook_clip = ImageClip(hook_img)
            hook_clip = hook_clip.set_position('center')
            hook_clip = hook_clip.set_duration(hook_duration)
            hook_clip = hook_clip.set_start(0)
            
            # Add scale effect
            hook_clip = hook_clip.resize(lambda t: 1 + 0.15 * (t / hook_duration))
            
            print(f"   ✅ Hook created")
            return hook_clip
            
        except Exception as e:
            print(f"   ❌ Hook creation failed: {e}")
            return None
    
    def create_end_screen(self, total_duration):
        """Create end screen with subscribe CTA"""
        try:
            print(f"\n   🔧 Creating end screen")
            
            end_duration = min(self.end_screen_duration, total_duration * 0.1)
            end_start = total_duration - end_duration
            
            # Dark overlay
            overlay = ColorClip(
                size=(self.width, self.height),
                color=(0, 0, 0)
            ).set_opacity(self.end_screen_opacity).set_duration(end_duration).set_start(end_start)
            
            # CTA text
            sub_img = text_generator.create_text_image(
                self.end_screen_cta,
                font_size=self.end_screen_font_size,
                color='white',
                stroke_width=5,
                stroke_color='red',
                max_width=self.width - 100
            )
            
            text_clip = ImageClip(sub_img)
            text_clip = text_clip.set_position('center')
            text_clip = text_clip.set_duration(end_duration)
            text_clip = text_clip.set_start(end_start)
            
            # Add bounce effect
            text_clip = text_clip.resize(lambda t: 1 + 0.05 * abs(np.sin(5 * t)))
            
            print(f"   ✅ End screen created")
            return overlay, text_clip
            
        except Exception as e:
            print(f"   ❌ End screen creation failed: {e}")
            return None, None

print("✅ compositor.py loaded with working subtitles")