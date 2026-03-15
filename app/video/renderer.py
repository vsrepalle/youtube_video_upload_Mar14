"""
Rendering module - STABILITY OPTIMIZED (SINGLE THREAD)
"""
import time
from pathlib import Path
from datetime import datetime
import traceback
import hashlib
import psutil

try:
    import config
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False

try:
    from moviepy import VideoFileClip
    RENDER_AVAILABLE = True
except ImportError as e:
    RENDER_AVAILABLE = False

class Renderer:
    def __init__(self, fps=24): # Reduced from 30 to 24 for 20% speed gain
        self.fps = fps
        self.render_timings = {}
        
        if CONFIG_AVAILABLE:
            self.ffmpeg_params = getattr(config, 'FFMPEG_PARAMS', [])
            self.audio_codec = getattr(config, 'AUDIO_CODEC', 'aac')
            self.audio_bitrate = getattr(config, 'AUDIO_BITRATE', '128k')
        else:
            self.ffmpeg_params = []
            self.audio_codec = 'aac'
            self.audio_bitrate = '128k'
        
        print("\n" + "="*60)
        print("⚡ [RENDER] STABILITY MODE: SINGLE THREAD")
        print("="*60)

    def render(self, video, output_path, duration, mode_settings=None, progress_callback=None):
        render_id = hashlib.md5(f"{time.time()}".encode()).hexdigest()[:6]
        
        if not RENDER_AVAILABLE or not video:
            return 0, 0
        
        render_start = time.time()
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Optimized params for speed and low CPU hang risk
            ffmpeg_params = [
                "-crf", "30",            # Lower quality slightly for massive speed boost
                "-preset", "ultrafast",  # Fastest possible encoding
                "-tune", "stillimage",   # Optimized for slideshow/news content
                "-movflags", "+faststart"
            ]
            
            print(f" 🚀 Rendering: {output_path}")
            
            video.write_videofile(
                output_path,
                fps=self.fps,
                codec="libx264",
                audio_codec=self.audio_codec,
                audio_bitrate=self.audio_bitrate,
                threads=1,               # CRITICAL: Prevents system hang
                preset="ultrafast",
                ffmpeg_params=ffmpeg_params,
                logger=progress_callback if progress_callback else 'bar',
                verbose=False
            )
            
            render_time = time.time() - render_start
            file_size = Path(output_path).stat().st_size / (1024 * 1024)
            
            self.render_timings[render_id] = {
                'duration': duration,
                'render_time': render_time,
                'file_size': file_size
            }
            
            return render_time, file_size
            
        except Exception as e:
            print(f"\n ❌ Render failed: {e}")
            traceback.print_exc()
            return 0, 0