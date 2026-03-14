# app/video/renderer.py - COMPLETE WITH PROGRESS CALLBACK SUPPORT
"""
Rendering module using mode-based settings (SINGLE SOURCE)
Includes progress callback support for main_video.py
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
    print("⚠️ [RENDER] Config not available")

try:
    from moviepy import VideoFileClip
    RENDER_AVAILABLE = True
except ImportError as e:
    RENDER_AVAILABLE = False
    print(f"⚠️ [RENDER] moviepy not available: {e}")

class Renderer:
    def __init__(self, fps=30):
        """Initialize renderer with debug"""
        self.fps = fps
        self.render_timings = {}
        
        # Read settings from config
        if CONFIG_AVAILABLE:
            self.ffmpeg_params = getattr(config, 'FFMPEG_PARAMS', [])
            self.audio_codec = getattr(config, 'AUDIO_CODEC', 'aac')
            self.audio_bitrate = getattr(config, 'AUDIO_BITRATE', '128k')
            self.audio_copy = getattr(config, 'AUDIO_COPY', False)
        else:
            self.ffmpeg_params = []
            self.audio_codec = 'aac'
            self.audio_bitrate = '128k'
            self.audio_copy = False
        
        print("\n" + "="*60)
        print("⚡ [RENDER] Initializing Renderer")
        print("="*60)
        print(f"   📊 FPS: {fps}")
        print(f"   💻 CPU Count: {psutil.cpu_count()}")
        print(f"   🎚️ Audio Copy: {self.audio_copy}")
        print(f"   ✅ Renderer initialized")
    
    def get_system_stats(self):
        """Get current system statistics"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        return {
            'cpu': cpu_percent,
            'memory_used': memory.percent,
            'memory_available': memory.available / (1024**3)
        }
    
    def get_settings_for_duration(self, duration):
        """Get optimal render settings based on duration (fallback)"""
        print(f"\n   ⚙️ [RENDER] Getting settings for {duration:.2f}s video")
        
        if duration < 30:
            settings = {
                'preset': 'ultrafast',
                'crf': 28,
                'threads': max(1, psutil.cpu_count() - 1),
                'bitrate': '2000k',
                'description': 'Fastest render for short videos'
            }
        elif duration < 60:
            settings = {
                'preset': 'superfast',
                'crf': 26,
                'threads': max(1, psutil.cpu_count() - 1),
                'bitrate': '3000k',
                'description': 'Balanced speed/quality'
            }
        else:
            settings = {
                'preset': 'veryfast',
                'crf': 24,
                'threads': max(1, psutil.cpu_count() - 2),
                'bitrate': '4000k',
                'description': 'Better quality for longer videos'
            }
        
        print(f"      📋 Selected: {settings['description']}")
        return settings
    
    def render(self, video, output_path, duration, mode_settings=None, progress_callback=None):
        """
        Render video with mode-based settings
        Args:
            video: MoviePy video clip
            output_path: Path to save video
            duration: Video duration in seconds
            mode_settings: Settings from config (TEST_SETTINGS, PRODUCTION_SETTINGS, etc.)
            progress_callback: Optional callback function for progress updates
        """
        render_id = hashlib.md5(f"{time.time()}".encode()).hexdigest()[:6]
        
        print("\n" + "="*70)
        print(f"⚡ [RENDER:{render_id}] STARTING RENDER")
        print("="*70)
        print(f"   📤 Output: {output_path}")
        print(f"   ⏱️ Video duration: {duration:.2f}s")
        
        # Get settings from mode (prioritize passed settings)
        if mode_settings:
            settings = mode_settings
        elif CONFIG_AVAILABLE:
            from config import get_render_settings, MODE
            settings = get_render_settings(MODE)
        else:
            # Fallback settings
            settings = {
                "preset": "ultrafast",
                "crf": 35,
                "threads": 2,
                "bitrate": "1000k",
                "description": "Fallback settings"
            }
        
        print(f"   🎚️ Mode: {settings['description']}")
        print(f"   🕒 Started at: {datetime.now().strftime('%H:%M:%S')}")
        
        stats_before = self.get_system_stats()
        print(f"\n   📊 System before render:")
        print(f"      CPU Usage: {stats_before['cpu']}%")
        print(f"      Memory Used: {stats_before['memory_used']}%")
        
        if not RENDER_AVAILABLE or not video:
            print("   ❌ Rendering disabled or no video - skipping")
            return 0, 0
        
        render_start = time.time()
        
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Build ffmpeg parameters
            ffmpeg_params = self.ffmpeg_params.copy()
            ffmpeg_params.extend([
                "-crf", str(settings['crf']),
                "-b:v", settings['bitrate'],
                "-maxrate", str(int(settings['bitrate'].replace('k','')) * 2) + 'k',
                "-bufsize", str(int(settings['bitrate'].replace('k','')) * 4) + 'k',
            ])
            
            # Add audio copy if enabled (faster)
            if self.audio_copy:
                ffmpeg_params.extend(["-c:a", "copy"])
            
            print(f"\n   🎬 Rendering with settings:")
            print(f"      Preset: {settings['preset']}")
            print(f"      CRF: {settings['crf']}")
            print(f"      Threads: {settings['threads']}")
            print(f"      Bitrate: {settings['bitrate']}")
            print(f"      Audio Copy: {self.audio_copy}")
            
            # Determine logger based on progress callback
            if progress_callback is not None:
                # Use custom progress callback
                logger = progress_callback
                print(f"   📊 Using custom progress bar")
            else:
                # Use built-in progress bar
                logger = 'bar'
                print(f"   📊 Using built-in progress bar")
            
            # Render video
            video.write_videofile(
                output_path,
                fps=self.fps,
                codec="libx264",
                audio_codec=self.audio_codec,
                audio_bitrate=self.audio_bitrate,
                threads=settings['threads'],
                preset=settings['preset'],
                ffmpeg_params=ffmpeg_params,
                logger=logger,
                verbose=False
            )
            
            render_time = time.time() - render_start
            file_size = Path(output_path).stat().st_size / (1024 * 1024)  # MB
            
            print(f"\n   ✅ RENDER COMPLETED at: {datetime.now().strftime('%H:%M:%S')}")
            print(f"   ⏱️ Render time: {render_time:.2f}s")
            print(f"   📏 File size: {file_size:.1f} MB")
            print(f"   ⚡ Speed: {duration/render_time:.2f}x realtime")
            
            # Store render timing
            self.render_timings[render_id] = {
                'duration': duration,
                'render_time': render_time,
                'file_size': file_size,
                'settings': settings,
                'speed_ratio': duration/render_time
            }
            
            print("="*70)
            return render_time, file_size
            
        except Exception as e:
            print(f"\n   ❌ Render failed: {e}")
            traceback.print_exc()
            return 0, 0
    
    def render_with_preset(self, video, output_path, duration, preset_name="test"):
        """
        Convenience method to render with a named preset
        Args:
            preset_name: "test", "production", or "ultra_fast"
        """
        if CONFIG_AVAILABLE:
            from config import get_render_settings
            settings = get_render_settings(preset_name)
        else:
            settings = None
        
        return self.render(video, output_path, duration, mode_settings=settings)
    
    def get_render_stats(self):
        """Get statistics about all renders performed"""
        if not self.render_timings:
            return "No renders completed yet"
        
        total_time = sum(t['render_time'] for t in self.render_timings.values())
        total_video = sum(t['duration'] for t in self.render_timings.values())
        avg_speed = total_video / total_time if total_time > 0 else 0
        
        stats = {
            'total_renders': len(self.render_timings),
            'total_render_time': total_time,
            'total_video_duration': total_video,
            'average_speed': avg_speed,
            'last_render': list(self.render_timings.values())[-1] if self.render_timings else None
        }
        
        print("\n" + "="*60)
        print("📊 RENDER STATISTICS")
        print("="*60)
        print(f"   Total renders: {stats['total_renders']}")
        print(f"   Total render time: {stats['total_render_time']:.2f}s")
        print(f"   Total video duration: {stats['total_video_duration']:.2f}s")
        print(f"   Average speed: {stats['average_speed']:.2f}x realtime")
        if stats['last_render']:
            last = stats['last_render']
            print(f"\n   Last render:")
            print(f"      Duration: {last['duration']:.2f}s")
            print(f"      Time: {last['render_time']:.2f}s")
            print(f"      Speed: {last['speed_ratio']:.2f}x")
            print(f"      Size: {last['file_size']:.1f} MB")
        print("="*60)
        
        return stats

print("\n✅ renderer.py loaded with progress callback support")