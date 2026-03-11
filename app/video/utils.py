# app/video/utils.py - WITH COMPREHENSIVE DEBUG LOGGING
"""
Utility functions with detailed debug logging
"""

import time
from pathlib import Path
import functools
import hashlib
import json
from datetime import datetime
import sys
import os

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class DebugTimer:
    """Context manager for timing code blocks with detailed debug"""
    
    def __init__(self, name, log_level="INFO"):
        self.name = name
        self.log_level = log_level
        self.start_time = None
        self.end_time = None
        self.id = hashlib.md5(f"{name}{time.time()}".encode()).hexdigest()[:4]
    
    def __enter__(self):
        self.start_time = time.time()
        self.start_memory = self._get_memory_usage()
        print(f"   ⏱️ [TIMER:{self.id}] Starting: {self.name}")
        return self
    
    def __exit__(self, *args):
        self.end_time = time.time()
        self.end_memory = self._get_memory_usage()
        self.duration = self.end_time - self.start_time
        memory_diff = self.end_memory - self.start_memory
        
        print(f"   ✅ [TIMER:{self.id}] Completed: {self.name}")
        print(f"      ⏱️ Duration: {self.duration:.3f}s")
        if memory_diff != 0:
            print(f"      🧠 Memory Δ: {memory_diff:+.1f}MB")
    
    def _get_memory_usage(self):
        """Get current memory usage in MB"""
        if PSUTIL_AVAILABLE:
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        return 0

def timeit(func):
    """Decorator to time functions with detailed debug"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_id = hashlib.md5(f"{func.__name__}{time.time()}".encode()).hexdigest()[:4]
        
        print(f"\n   ⏱️ [TIMER:{func_id}] Calling: {func.__name__}")
        start = time.time()
        
        if PSUTIL_AVAILABLE:
            process = psutil.Process()
            mem_before = process.memory_info().rss / 1024 / 1024
        
        result = func(*args, **kwargs)
        
        end = time.time()
        duration = end - start
        
        if PSUTIL_AVAILABLE:
            mem_after = process.memory_info().rss / 1024 / 1024
            mem_diff = mem_after - mem_before
            print(f"   ✅ [TIMER:{func_id}] {func.__name__} completed")
            print(f"      ⏱️ Duration: {duration:.3f}s")
            print(f"      🧠 Memory: {mem_before:.1f}MB → {mem_after:.1f}MB (Δ: {mem_diff:+.1f}MB)")
        else:
            print(f"   ✅ [TIMER:{func_id}] {func.__name__} completed in {duration:.3f}s")
        
        return result
    return wrapper

def log_memory(func):
    """Decorator to log memory usage with debug"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if PSUTIL_AVAILABLE:
            process = psutil.Process()
            mem_before = process.memory_info().rss / 1024 / 1024
            cpu_before = process.cpu_percent(interval=0.1)
            
            print(f"\n   📊 [MEMORY] Before {func.__name__}:")
            print(f"      Memory: {mem_before:.1f}MB")
            print(f"      CPU: {cpu_before:.1f}%")
        
        result = func(*args, **kwargs)
        
        if PSUTIL_AVAILABLE:
            mem_after = process.memory_info().rss / 1024 / 1024
            cpu_after = process.cpu_percent(interval=0.1)
            mem_diff = mem_after - mem_before
            
            print(f"   📊 [MEMORY] After {func.__name__}:")
            print(f"      Memory: {mem_after:.1f}MB (Δ: {mem_diff:+.1f}MB)")
            print(f"      CPU: {cpu_after:.1f}%")
            
            if mem_diff > 100:
                print(f"      ⚠️ High memory increase!")
        
        return result
    return wrapper

class Timer:
    """Simple context manager for timing code blocks"""
    
    def __init__(self, name):
        self.name = name
        self.start = None
        self.end = None
    
    def __enter__(self):
        self.start = time.time()
        print(f"   ⏱️ Starting: {self.name}")
        return self
    
    def __exit__(self, *args):
        self.end = time.time()
        self.duration = self.end - self.start
        print(f"   ✅ Completed: {self.name} ({self.duration:.2f}s)")

def ensure_dir(path):
    """Ensure directory exists with debug"""
    path = Path(path)
    if not path.exists():
        print(f"   📁 Creating directory: {path}")
        path.mkdir(parents=True, exist_ok=True)
        print(f"      ✅ Created")
    else:
        print(f"   📁 Directory exists: {path}")
    return path

def format_bytes(bytes_val):
    """Format bytes to human readable with debug"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024:
            formatted = f"{bytes_val:.1f}{unit}"
            print(f"   📊 Size: {formatted}")
            return formatted
        bytes_val /= 1024
    formatted = f"{bytes_val:.1f}TB"
    print(f"   📊 Size: {formatted}")
    return formatted

def get_file_info(file_path):
    """Get detailed file information with debug"""
    path = Path(file_path)
    if not path.exists():
        print(f"   ❌ File not found: {file_path}")
        return None
    
    stat = path.stat()
    info = {
        'name': path.name,
        'size': stat.st_size,
        'size_hr': format_bytes(stat.st_size),
        'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        'extension': path.suffix
    }
    
    print(f"\n   📄 File info for {path.name}:")
    print(f"      Size: {info['size_hr']}")
    print(f"      Created: {info['created']}")
    print(f"      Modified: {info['modified']}")
    
    return info

def debug_print_video_info(video_clip):
    """Print detailed video clip information"""
    print("\n   🎬 Video Clip Info:")
    print(f"      Duration: {video_clip.duration:.2f}s")
    print(f"      Size: {video_clip.size}")
    print(f"      FPS: {video_clip.fps if hasattr(video_clip, 'fps') else 'N/A'}")
    print(f"      Audio: {'Yes' if video_clip.audio else 'No'}")
    
    if hasattr(video_clip, 'audio') and video_clip.audio:
        print(f"      Audio Duration: {video_clip.audio.duration:.2f}s")

def check_system_resources():
    """Check and log system resources"""
    print("\n   💻 System Resources:")
    
    if PSUTIL_AVAILABLE:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        print(f"      CPU Usage: {cpu_percent}%")
        print(f"      Memory: {memory.used / (1024**3):.1f}GB / {memory.total / (1024**3):.1f}GB ({memory.percent}%)")
        print(f"      Disk: {disk.used / (1024**3):.1f}GB / {disk.total / (1024**3):.1f}GB ({disk.percent}%)")
        print(f"      Available Memory: {memory.available / (1024**3):.1f}GB")
    else:
        print("      psutil not available - install for detailed system info")
    
    return True

print("\n✅ utils.py loaded with comprehensive debug")