# app/video/audio.py - WITH COMPREHENSIVE DEBUG LOGGING
"""
Audio handling module with detailed debug logging
"""

from pathlib import Path
import time
import traceback
import hashlib
from datetime import datetime

try:
    from moviepy.editor import AudioFileClip
    AUDIO_AVAILABLE = True
except ImportError as e:
    AUDIO_AVAILABLE = False
    print(f"⚠️ [AUDIO] moviepy not available: {e}")

def load_audio(audio_path, duration=None):
    """
    Load audio file and return clip and duration with comprehensive debug
    """
    audio_id = hashlib.md5(f"{audio_path}{time.time()}".encode()).hexdigest()[:4]
    
    print(f"\n🔊 [AUDIO:{audio_id}] Loading audio...")
    print(f"   Path: {audio_path}")
    print(f"   Requested duration: {duration if duration else 'full'}")
    print(f"   Started at: {datetime.now().strftime('%H:%M:%S')}")
    
    start_time = time.time()
    
    # Check if file exists
    if not audio_path or not Path(audio_path).exists():
        print(f"   ❌ [AUDIO:{audio_id}] File not found: {audio_path}")
        return None, None
    
    file_size = Path(audio_path).stat().st_size / (1024 * 1024)
    print(f"   📊 File size: {file_size:.2f} MB")
    
    if not AUDIO_AVAILABLE:
        print(f"   ⚠️ [AUDIO:{audio_id}] moviepy not installed - returning dummy")
        return None, 30
    
    try:
        # Load audio
        load_start = time.time()
        print(f"   🔄 Loading audio file...")
        audio = AudioFileClip(audio_path)
        audio_duration = audio.duration
        load_time = time.time() - load_start
        
        print(f"   ✅ [AUDIO:{audio_id}] Loaded successfully:")
        print(f"      Duration: {audio_duration:.2f}s")
        print(f"      FPS: {audio.fps if hasattr(audio, 'fps') else 'N/A'}")
        print(f"      Channels: {audio.nchannels if hasattr(audio, 'nchannels') else 'N/A'}")
        print(f"      Load time: {load_time:.2f}s")
        
        # Trim if duration specified
        if duration and audio_duration > duration:
            print(f"   ✂️ Trimming from {audio_duration:.2f}s to {duration:.2f}s")
            audio = audio.subclip(0, duration)
            audio_duration = duration
            print(f"      ✅ Trimmed")
        
        total_time = time.time() - start_time
        print(f"   ✅ [AUDIO:{audio_id}] Complete (total: {total_time:.2f}s)")
        
        return audio, audio_duration
        
    except Exception as e:
        print(f"   ❌ [AUDIO:{audio_id}] Error loading audio: {e}")
        traceback.print_exc()
        return None, None

def estimate_duration_from_text(text, words_per_second=2.5):
    """
    Estimate video duration from text length with debug
    """
    print(f"\n📝 [DURATION] Estimating duration from text...")
    
    word_count = len(text.split())
    duration = max(15, min(60, word_count / words_per_second))
    
    print(f"   📊 Word count: {word_count}")
    print(f"   ⏱️ Estimated duration: {duration:.2f}s")
    print(f"      (based on {words_per_second} words/sec)")
    
    return duration

def create_silent_audio(duration, output_path="audio/silent.mp3"):
    """
    Create silent audio file as fallback with debug
    """
    print(f"\n🔇 [AUDIO] Creating silent audio:")
    print(f"   Duration: {duration}s")
    print(f"   Output: {output_path}")
    
    try:
        import numpy as np
        from scipy.io import wavfile
        
        sample_rate = 44100
        output_wav = Path(output_path).with_suffix('.wav')
        
        # Create silent WAV file
        print(f"   🔄 Generating silent WAV...")
        with wave.open(str(output_wav), 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b'\x00\x00' * sample_rate * duration)
        
        file_size = output_wav.stat().st_size / (1024 * 1024)
        print(f"   ✅ Created: {output_wav} ({file_size:.2f} MB)")
        
        return str(output_wav)
        
    except Exception as e:
        print(f"   ❌ Failed to create silent audio: {e}")
        return None

def get_audio_info(audio_path):
    """Get detailed audio file information with debug"""
    if not Path(audio_path).exists():
        print(f"   ❌ Audio file not found: {audio_path}")
        return None
    
    print(f"\n📊 [AUDIO] Getting info for: {audio_path}")
    
    try:
        audio = AudioFileClip(audio_path)
        info = {
            'duration': audio.duration,
            'fps': audio.fps if hasattr(audio, 'fps') else 'N/A',
            'channels': audio.nchannels if hasattr(audio, 'nchannels') else 'N/A',
            'size': Path(audio_path).stat().st_size / (1024 * 1024)
        }
        
        print(f"   Duration: {info['duration']:.2f}s")
        print(f"   FPS: {info['fps']}")
        print(f"   Channels: {info['channels']}")
        print(f"   Size: {info['size']:.2f} MB")
        
        audio.close()
        return info
        
    except Exception as e:
        print(f"   ❌ Error getting audio info: {e}")
        return None

print("\n✅ audio.py loaded with comprehensive debug")