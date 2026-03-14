# app/video/text.py - WITH DETAILED DEBUG LOGGING
"""
Text generation module with caching and comprehensive debug
"""

# app/video/text.py - VERSION 1.0 (STABLE)
"""
Text generation module with caching and comprehensive debug
STABLE VERSION: Basic text rendering without highlighting

VERSION HISTORY:
v1.0 (2026-03-14): Stable text rendering system
    - Basic text image creation with PIL
    - Font caching and error handling
    - No word highlighting features

v0.9 (2026-03-14): Attempted word highlighting (REVERTED)
    - Added create_text_with_highlight method
    - Tried to highlight individual words in sentences
    - REVERTED due to rendering complexity
"""

import numpy as np
import hashlib
import time
import traceback
from datetime import datetime

try:
    from PIL import Image, ImageDraw, ImageFont
    TEXT_AVAILABLE = True
    print("✅ [TEXT] PIL available for text generation")
except ImportError as e:
    TEXT_AVAILABLE = False
    print(f"❌ [TEXT] PIL not available: {e}")

class TextGenerator:
    def __init__(self):
        """Initialize text generator with caching"""
        self._cache = {}
        self._font_cache = {}
        self.debug_timings = {}
        
        print("\n" + "="*60)
        print("📝 [TEXT] Initializing TextGenerator")
        print("="*60)
        
        # Load config if available
        try:
            import config
            self.default_font_size = getattr(config, 'SUBTITLE_FONT_SIZE', 54)
            self.default_color = getattr(config, 'SUBTITLE_COLOR', 'yellow')
            print(f"   ✅ [TEXT] Loaded from config: font_size={self.default_font_size}, color={self.default_color}")
        except ImportError:
            self.default_font_size = 54
            self.default_color = 'yellow'
            print(f"   ⚠️ [TEXT] Config not found, using defaults: {self.default_font_size}, {self.default_color}")
        except Exception as e:
            self.default_font_size = 54
            self.default_color = 'yellow'
            print(f"   ⚠️ [TEXT] Error loading config: {e}")
        
        print(f"   📊 [TEXT] Cache initialized: empty")
        print("✅ [TEXT] TextGenerator initialized")
    
    def _get_font(self, font_size):
        """Get font with caching and detailed debug"""
        debug_start = time.time()
        cache_key = f"font_{font_size}"
        
        print(f"\n   🔍 [FONT] Getting font size {font_size}")
        
        # Check cache first
        if cache_key in self._font_cache:
            print(f"      ✅ [FONT] Using cached font (found in cache)")
            return self._font_cache[cache_key]
        
        print(f"      ⚠️ [FONT] Font not in cache, attempting to load...")
        
        if not TEXT_AVAILABLE:
            print(f"      ❌ [FONT] PIL not available - returning None")
            return None
        
        # Try different font paths
        font_paths = [
            "arial.ttf",
            "Arial",
            "C:\\Windows\\Fonts\\arial.ttf",
            "C:\\Windows\\Fonts\\Arial.ttf",
            "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/Library/Fonts/Arial.ttf"
        ]
        
        for path in font_paths:
            try:
                print(f"      🔍 [FONT] Trying path: {path}")
                font = ImageFont.truetype(path, font_size)
                self._font_cache[cache_key] = font
                print(f"      ✅ [FONT] Found font at: {path}")
                print(f"      ⏱️  [FONT] Font loading took: {time.time()-debug_start:.3f}s")
                return font
            except Exception as e:
                print(f"      ⚠️ [FONT] Failed at {path}: {str(e)[:50]}...")
                continue
        
        # Fallback to default
        print(f"      ⚠️ [FONT] No TrueType font found, using default")
        try:
            font = ImageFont.load_default()
            self._font_cache[cache_key] = font
            print(f"      ✅ [FONT] Default font loaded")
            return font
        except Exception as e:
            print(f"      ❌ [FONT] Even default font failed: {e}")
            return None
    
    def create_text_image(self, text, font_size, color, stroke_width=0, 
                         stroke_color='black', max_width=900, max_height=None):
        """
        Create text as PIL image with caching and comprehensive debug
        """
        debug_id = hashlib.md5(f"{time.time()}".encode()).hexdigest()[:6]
        start_time = time.time()
        
        print(f"\n   📝 [TEXT:{debug_id}] Creating text: '{text[:50]}...'")
        print(f"      Settings: font={font_size}, color={color}, stroke={stroke_width}")
        print(f"      Max dimensions: {max_width}x{max_height if max_height else 'auto'}")
        
        if not TEXT_AVAILABLE:
            print(f"      ❌ [TEXT:{debug_id}] PIL not available - returning dummy image")
            return np.zeros((100, max_width, 4), dtype=np.uint8)
        
        # Create cache key
        key_str = f"{text}_{font_size}_{color}_{stroke_width}_{stroke_color}_{max_width}"
        cache_key = hashlib.md5(key_str.encode()).hexdigest()
        
        if cache_key in self._cache:
            print(f"      ✅ [TEXT:{debug_id}] Using cached text image (hit)")
            cache_time = time.time() - start_time
            print(f"      ⏱️  [TEXT:{debug_id}] Cache retrieval: {cache_time:.3f}s")
            return self._cache[cache_key].copy()
        
        print(f"      ⚠️ [TEXT:{debug_id}] Cache miss, generating new text image")
        
        try:
            # Get font
            font = self._get_font(font_size)
            if not font:
                print(f"      ❌ [TEXT:{debug_id}] Font not available - returning dummy")
                return np.zeros((100, max_width, 4), dtype=np.uint8)
            
            # Create temp image to measure text
            measure_start = time.time()
            print(f"      📏 [TEXT:{debug_id}] Measuring text size...")
            temp_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
            temp_draw = ImageDraw.Draw(temp_img)
            
            # Get text size using different methods for compatibility
            try:
                # Method 1: textbbox (PIL 8.0.0+)
                bbox = temp_draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            except AttributeError:
                # Method 2: textsize (older PIL)
                text_width, text_height = temp_draw.textsize(text, font=font)
            
            print(f"      📏 [TEXT:{debug_id}] Measured: {text_width}x{text_height} (took {time.time()-measure_start:.3f}s)")
            
            # Scale down if too wide
            if text_width > max_width and font_size > 20:
                scale = max_width / text_width
                new_size = int(font_size * scale * 0.9)
                print(f"      ⚠️ [TEXT:{debug_id}] Text too wide ({text_width} > {max_width})")
                print(f"      🔄 [TEXT:{debug_id}] Scaling down to font size {new_size}")
                return self.create_text_image(text, new_size, color, stroke_width,
                                            stroke_color, max_width, max_height)
            
            # Add padding
            padding = stroke_width * 2 + 20
            img_width = min(text_width + padding, max_width)
            img_height = text_height + padding
            if max_height:
                img_height = min(img_height, max_height)
            
            print(f"      📏 [TEXT:{debug_id}] Final image size: {img_width}x{img_height}")
            
            # Create image
            create_start = time.time()
            img = Image.new('RGBA', (int(img_width), int(img_height)), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Position text
            x = (img_width - text_width) // 2
            y = (img_height - text_height) // 2
            print(f"      📍 [TEXT:{debug_id}] Text position: ({x:.1f}, {y:.1f})")
            
            # Draw stroke
            if stroke_width > 0:
                print(f"      ✏️ [TEXT:{debug_id}] Drawing stroke width {stroke_width}")
                stroke_start = time.time()
                for dx in [-stroke_width, 0, stroke_width]:
                    for dy in [-stroke_width, 0, stroke_width]:
                        if dx != 0 or dy != 0:
                            draw.text((x + dx, y + dy), text, font=font, fill=stroke_color)
                print(f"      ⏱️  [TEXT:{debug_id}] Stroke drawing: {time.time()-stroke_start:.3f}s")
            
            # Draw main text
            text_start = time.time()
            draw.text((x, y), text, font=font, fill=color)
            print(f"      ⏱️  [TEXT:{debug_id}] Main text drawing: {time.time()-text_start:.3f}s")
            
            # Convert to numpy array
            convert_start = time.time()
            result = np.array(img)
            print(f"      ⏱️  [TEXT:{debug_id}] NumPy conversion: {time.time()-convert_start:.3f}s")
            
            # Cache the result
            self._cache[cache_key] = result
            cache_size = len(self._cache)
            
            total_time = time.time() - start_time
            print(f"      ✅ [TEXT:{debug_id}] Text created successfully")
            print(f"      ⏱️  [TEXT:{debug_id}] Total time: {total_time:.3f}s")
            print(f"      📊 [TEXT:{debug_id}] Cache size now: {cache_size}")
            
            return result
            
        except Exception as e:
            print(f"      ❌ [TEXT:{debug_id}] Error: {e}")
            traceback.print_exc()
            return np.zeros((100, max_width, 4), dtype=np.uint8)
    
    def clear_cache(self):
        """Clear text cache with debug"""
        cache_size = len(self._cache)
        font_cache_size = len(self._font_cache)
        
        print(f"\n🧹 [TEXT] Clearing cache...")
        print(f"   📊 Before: {cache_size} text, {font_cache_size} font entries")
        
        self._cache.clear()
        self._font_cache.clear()
        
        print(f"   ✅ [TEXT] Cache cleared")
        print(f"   📊 After: {len(self._cache)} text, {len(self._font_cache)} font entries")
    
    def get_cache_stats(self):
        """Get cache statistics"""
        return {
            'text_cache': len(self._cache),
            'font_cache': len(self._font_cache),
            'text_cache_keys': list(self._cache.keys())[:5] if self._cache else []
        }

# Singleton instance
text_generator = TextGenerator()

# Print final initialization status
print("\n" + "="*60)
print("📊 [TEXT] Final Status:")
print(f"   PIL Available: {TEXT_AVAILABLE}")
print(f"   Text Cache: {len(text_generator._cache)} entries")
print(f"   Font Cache: {len(text_generator._font_cache)} entries")
print("="*60)
print("✅ text.py loaded with comprehensive debug")