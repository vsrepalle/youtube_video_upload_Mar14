# app/config.py - COMPLETE WITH ALL SETTINGS
"""
Configuration settings for video generation
CHANGE ONLY THIS FILE to customize all aspects
"""
# Add this to your config.py (anywhere, but preferably near the top)
IMAGEMAGICK_BINARY = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

# app/config.py

# For Cricket & Bollywood (SpaceMind_AI uses this if keywords match)
SERPAPI_KEY = "your_serpapi_key_here"

# For Space, Gadgets, and Education
PEXELS_API_KEY = "Oszdsq7V3DU1S8t1n6coHlHHeHb76cxZjb1HRYYvru32CpQYSmrO52ax"
# ───────────────────────────────────────────────
# VIDEO SETTINGS - Core dimensions
# ───────────────────────────────────────────────

# Resolution for YouTube Shorts (vertical 9:16)
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 30

# YouTube Shorts limit (180 seconds)
SHORTS_MAX_DURATION = 180

# ───────────────────────────────────────────────
# IMAGE DISPLAY SETTINGS - Controls how images appear
# ───────────────────────────────────────────────

# How images are fitted to frame
# "cover" - Fill entire frame (may crop) - BEST for full screen
# "contain" - Show entire image (adds black bars)
# "zoom" - Fill with subtle zoom effect
IMAGE_FIT_MODE = "cover"

# Zoom effect settings (when IMAGE_FIT_MODE = "zoom")
ZOOM_START_SCALE = 1.0
ZOOM_END_SCALE = 1.15  # 15% zoom for subtle motion

# Image display duration (seconds per image)
IMAGE_DISPLAY_DURATION = 3.5

# Transition between images
TRANSITION_ENABLED = True
TRANSITION_DURATION = 0.5  # Crossfade duration

# ───────────────────────────────────────────────
# HEADER SETTINGS - Top banner with headline
# ───────────────────────────────────────────────

# Header visibility
HEADER_ENABLED = True
HEADER_HEIGHT = 180  # Tall header for visibility
HEADER_OPACITY = 0.85  # Semi-transparent

# Header text settings
HEADER_FONT_SIZE = 85  # Large font for readability
HEADER_FONT_COLOR = "white"
HEADER_STROKE_COLOR = "black"
HEADER_STROKE_WIDTH = 4  # Thick stroke for contrast

# Header background
HEADER_BG_COLOR = (0, 0, 0)
HEADER_GRADIENT = True  # Gradient background looks better
HEADER_TEXT_POSITION = 50  # Pixels from top

# ───────────────────────────────────────────────
# SUBTITLE SETTINGS - Lower third text
# ───────────────────────────────────────────────

# Subtitle visibility
SUBTITLE_ENABLED = True
SUBTITLE_FONT_SIZE = 70
SUBTITLE_COLOR = "yellow"
SUBTITLE_STROKE_COLOR = "black"
SUBTITLE_STROKE_WIDTH = 4

# Subtitle position
SUBTITLE_Y_POSITION = 1650  # 270px from bottom of 1920
SUBTITLE_MAX_WIDTH = 900

# Subtitle timing adjustments (critical for sync)
SUBTITLE_DISPLAY_RATIO = 0.9  # Show for 90% of chunk duration
SUBTITLE_FADE_IN = 0.2
SUBTITLE_FADE_OUT = 0.2
SUBTITLE_EXTRA_START = 0.1  # Start slightly before audio
SUBTITLE_EXTRA_END = 0.1    # End slightly after audio

# Subtitle chunking
SUBTITLE_WORDS_PER_CHUNK = 4  # Smaller chunks for better sync
SUBTITLE_MAX_CHUNKS = 15

# ───────────────────────────────────────────────
# HOOK SETTINGS - Opening attention-grabber
# ───────────────────────────────────────────────

HOOK_ENABLED = True
HOOK_FONT_SIZE = 110
HOOK_COLOR = "yellow"
HOOK_STROKE_COLOR = "black"
HOOK_STROKE_WIDTH = 6
HOOK_DURATION = 3.0
HOOK_FADE_OUT = True
HOOK_MAX_WIDTH = 900

# ───────────────────────────────────────────────
# END SCREEN SETTINGS - Subscribe call-to-action
# ───────────────────────────────────────────────

END_SCREEN_ENABLED = True
END_SCREEN_DURATION = 4.0
END_SCREEN_OPACITY = 0.85
END_SCREEN_FONT_SIZE = 95
END_SCREEN_TEXT_COLOR = "white"
END_SCREEN_STROKE_COLOR = "red"
END_SCREEN_STROKE_WIDTH = 5
END_SCREEN_MAX_WIDTH = 900
END_SCREEN_CTA = "🔔 SUBSCRIBE FOR MORE!"

# ───────────────────────────────────────────────
# RENDERING MODES - Speed vs Quality
# ───────────────────────────────────────────────

# Current mode: "test", "production", or "ultra_fast"
MODE = "test"

# Test mode - Fast rendering for testing
TEST_SETTINGS = {
    "fps": 20,
    "preset": "ultrafast",
    "crf": 35,
    "threads": 4,
    "bitrate": "1000k",
    "resolution_scale": 1.0,
    "description": "TEST MODE - Fast rendering"
}

# Production mode - High quality for final videos
PRODUCTION_SETTINGS = {
    "fps": 30,
    "preset": "faster",
    "crf": 23,
    "threads": 8,
    "bitrate": "5000k",
    "resolution_scale": 1.0,
    "description": "PRODUCTION MODE - High quality"
}

# Ultra fast mode - Maximum speed for quick tests
ULTRA_FAST_SETTINGS = {
    "fps": 15,
    "preset": "ultrafast",
    "crf": 45,
    "threads": 8,
    "bitrate": "500k",
    "resolution_scale": 0.75,  # 810x1440 - 4x faster
    "description": "ULTRA FAST - Maximum speed"
}

# ───────────────────────────────────────────────
# PROGRESS BAR SETTINGS - Visual feedback during render
# ───────────────────────────────────────────────

PROGRESS_BAR_ENABLED = True
PROGRESS_BAR_STYLE = "detailed"  # "simple" or "detailed"
PROGRESS_BAR_LENGTH = 50
PROGRESS_BAR_UPDATE_INTERVAL = 0.5  # seconds

# ───────────────────────────────────────────────
# YOUTUBE UPLOAD SETTINGS
# ───────────────────────────────────────────────

# Enable/disable auto-upload after generation
AUTO_UPLOAD_ENABLED = False

# YouTube API credentials file (download from Google Cloud Console)
YOUTUBE_CLIENT_SECRETS_FILE = "client_secret.json"

# Default upload settings
UPLOAD_DEFAULTS = {
    "privacy_status": "private",  # "private", "unlisted", or "public"
    "category_id": "22",          # 22 = People & Blogs
    "language": "en",
    "embeddable": True,
    "license": "youtube",
    "made_for_kids": False,
}

# Default tags for all uploads
DEFAULT_TAGS = ["trendwavenow", "viral", "trending", "news", "shorts"]

# ───────────────────────────────────────────────
# DEBUG SETTINGS
# ───────────────────────────────────────────────

DEBUG_MODE = True
LOG_PERFORMANCE = True
VERBOSE_OUTPUT = True

# ───────────────────────────────────────────────
# HELPER FUNCTIONS - DO NOT CHANGE
# ───────────────────────────────────────────────

def get_image_settings():
    """Get all image display settings"""
    return {
        "fit_mode": IMAGE_FIT_MODE,
        "zoom_start": ZOOM_START_SCALE,
        "zoom_end": ZOOM_END_SCALE,
        "duration": IMAGE_DISPLAY_DURATION,
        "transition": TRANSITION_ENABLED,
        "transition_duration": TRANSITION_DURATION
    }

def get_header_settings():
    """Get all header settings"""
    return {
        "enabled": HEADER_ENABLED,
        "height": HEADER_HEIGHT,
        "opacity": HEADER_OPACITY,
        "font_size": HEADER_FONT_SIZE,
        "font_color": HEADER_FONT_COLOR,
        "stroke_color": HEADER_STROKE_COLOR,
        "stroke_width": HEADER_STROKE_WIDTH,
        "bg_color": HEADER_BG_COLOR,
        "gradient": HEADER_GRADIENT,
        "text_position": HEADER_TEXT_POSITION
    }

def get_subtitle_settings():
    """Get all subtitle settings"""
    return {
        "enabled": SUBTITLE_ENABLED,
        "font_size": SUBTITLE_FONT_SIZE,
        "color": SUBTITLE_COLOR,
        "stroke_color": SUBTITLE_STROKE_COLOR,
        "stroke_width": SUBTITLE_STROKE_WIDTH,
        "y_position": SUBTITLE_Y_POSITION,
        "max_width": SUBTITLE_MAX_WIDTH,
        "display_ratio": SUBTITLE_DISPLAY_RATIO,
        "fade_in": SUBTITLE_FADE_IN,
        "fade_out": SUBTITLE_FADE_OUT,
        "extra_start": SUBTITLE_EXTRA_START,
        "extra_end": SUBTITLE_EXTRA_END,
        "words_per_chunk": SUBTITLE_WORDS_PER_CHUNK,
        "max_chunks": SUBTITLE_MAX_CHUNKS
    }

def get_progress_bar_settings():
    """Get progress bar settings"""
    return {
        "enabled": PROGRESS_BAR_ENABLED,
        "style": PROGRESS_BAR_STYLE,
        "length": PROGRESS_BAR_LENGTH,
        "update_interval": PROGRESS_BAR_UPDATE_INTERVAL
    }

def is_shorts_eligible(duration):
    """Check if video qualifies as a YouTube Short"""
    return duration <= SHORTS_MAX_DURATION

def get_render_settings(mode=None):
    """Get render settings based on mode"""
    if mode == "production":
        return PRODUCTION_SETTINGS
    elif mode == "ultra_fast":
        return ULTRA_FAST_SETTINGS
    else:
        return TEST_SETTINGS

def set_mode(mode):
    """Switch between rendering modes"""
    global MODE, ACTIVE_SETTINGS, FPS
    MODE = mode
    ACTIVE_SETTINGS = get_render_settings(mode)
    FPS = ACTIVE_SETTINGS["fps"]
    print(f"\n🔄 Switched to {mode.upper()} mode")
    print(f"   {ACTIVE_SETTINGS['description']}")
    print(f"   FPS: {FPS}, Preset: {ACTIVE_SETTINGS['preset']}, Bitrate: {ACTIVE_SETTINGS['bitrate']}")

def get_upload_settings():
    """Get YouTube upload settings"""
    return {
        "enabled": AUTO_UPLOAD_ENABLED,
        "client_secrets": YOUTUBE_CLIENT_SECRETS_FILE,
        "defaults": UPLOAD_DEFAULTS,
        "default_tags": DEFAULT_TAGS,
    }

# Active settings (used by other modules)
ACTIVE_SETTINGS = get_render_settings(MODE)
FPS = ACTIVE_SETTINGS["fps"]

print("="*70)
print(f"✅ CONFIG LOADED - {MODE.upper()} MODE")
print(f"   Resolution: {VIDEO_WIDTH}x{VIDEO_HEIGHT}")
print(f"   Image Fit: {IMAGE_FIT_MODE}")
print(f"   Header Size: {HEADER_FONT_SIZE}px")
print(f"   Subtitle Sync: {SUBTITLE_DISPLAY_RATIO}x speed")
print(f"   Progress Bar: {'ON' if PROGRESS_BAR_ENABLED else 'OFF'}")
print(f"   Auto-Upload: {'ON' if AUTO_UPLOAD_ENABLED else 'OFF'}")
print("="*70)