#!/usr/bin/env python
# run_interactive.py - COMPLETE INTERACTIVE VIDEO GENERATOR
"""
Interactive Video Generator - All-in-one script
Run this file and answer the prompts to generate videos
Includes mode selection, preview, and YouTube upload
"""

import sys
import os
from pathlib import Path
import json
import time
import subprocess
from datetime import datetime
import hashlib
import platform
import shutil

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import config for settings
try:
    from app.config import (
        VIDEO_WIDTH, VIDEO_HEIGHT, SHORTS_MAX_DURATION, 
        MODES, AUTO_UPLOAD_ENABLED, get_upload_settings
    )
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    # Fallback values
    VIDEO_WIDTH = 1080
    VIDEO_HEIGHT = 1920
    SHORTS_MAX_DURATION = 180
    AUTO_UPLOAD_ENABLED = False

# ============================================
# UTILITY FUNCTIONS
# ============================================

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"🎬 {title}".center(70))
    print("="*70)

def print_step(step, message):
    """Print a step message"""
    print(f"\n📌 STEP {step}: {message}")

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_warning(message):
    """Print warning message"""
    print(f"⚠️  {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ️  {message}")

def format_time(seconds):
    """Format time in seconds to readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

def get_user_choice(prompt, options):
    """Get user choice from options"""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"   {i}. {option}")
    
    while True:
        try:
            choice = input("\n👉 Enter your choice (number): ").strip()
            if not choice:
                continue
            choice = int(choice)
            if 1 <= choice <= len(options):
                return choice
            else:
                print_error(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print_error("Please enter a valid number")

def get_user_input(prompt, default=None):
    """Get user input with default"""
    if default:
        value = input(f"\n👉 {prompt} [{default}]: ").strip()
        return value if value else default
    else:
        return input(f"\n👉 {prompt}: ").strip()

def confirm_action(prompt):
    """Ask for user confirmation"""
    response = input(f"\n👉 {prompt} (y/n): ").lower().strip()
    return response == 'y' or response == 'yes'

# ============================================
# PROGRESS BAR
# ============================================

class ProgressBar:
    """Simple progress bar for visual feedback"""
    def __init__(self, total, prefix='', suffix='', length=40):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.start_time = time.time()
    
    def update(self, iteration):
        percent = iteration / self.total
        arrow = '█' * int(round(self.length * percent))
        spaces = ' ' * (self.length - len(arrow))
        elapsed = time.time() - self.start_time
        
        if percent > 0:
            eta = (elapsed / percent) - elapsed
            eta_str = format_time(eta)
        else:
            eta_str = "calculating..."
        
        print(f'\r{self.prefix} |{arrow}{spaces}| {percent:.1%} {self.suffix} [⏱️ {format_time(elapsed)} ETA: {eta_str}]', end='\r')
        if iteration == self.total:
            print()

# ============================================
# VIDEO PREVIEW FUNCTION
# ============================================

def preview_video(video_path):
    """Preview the generated video"""
    print_header("🎬 VIDEO PREVIEW")
    
    if not Path(video_path).exists():
        print_error("Video file not found!")
        return False
    
    file_size = Path(video_path).stat().st_size / (1024 * 1024)
    print_info(f"File: {video_path.name}")
    print_info(f"Size: {file_size:.2f} MB")
    
    # Get video info using ffprobe if available
    try:
        import subprocess
        result = subprocess.run([
            'ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams',
            str(video_path)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            info = json.loads(result.stdout)
            for stream in info.get('streams', []):
                if stream.get('codec_type') == 'video':
                    print_info(f"Resolution: {stream.get('width')}x{stream.get('height')}")
                    print_info(f"Duration: {float(info['format'].get('duration', 0)):.1f}s")
                    print_info(f"Bitrate: {int(info['format'].get('bit_rate', 0))//1000}k")
                    break
    except:
        pass
    
    print("\n🎥 Preview options:")
    print("   1. Play video (opens with default player)")
    print("   2. Show video info only")
    print("   3. Skip preview")
    
    choice = get_user_choice("Choose preview option:", ["Play video", "Show info only", "Skip preview"])
    
    if choice == 1:
        # Open with default player
        try:
            if platform.system() == 'Windows':
                os.startfile(video_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', video_path])
            else:  # Linux
                subprocess.run(['xdg-open', video_path])
            print_success("Video player opened")
        except Exception as e:
            print_error(f"Could not open video: {e}")
    
    return True

# ============================================
# YOUTUBE UPLOAD FUNCTION
# ============================================

def upload_to_youtube(video_path, json_data):
    """Upload video to YouTube"""
    print_header("📤 YOUTUBE UPLOAD")
    
    if not Path(video_path).exists():
        print_error("Video file not found!")
        return False
    
    try:
        # Import upload module
        from upload_to_youtube import YouTubeUploader
        
        print_info(f"Uploading: {video_path.name}")
        print_info(f"Title: {json_data.get('headline', 'Untitled')[:60]}...")
        
        uploader = YouTubeUploader()
        
        # Ask for privacy setting
        print("\nPrivacy options:")
        print("   1. Private (only you can see)")
        print("   2. Unlisted (anyone with link can see)")
        print("   3. Public (everyone can see)")
        
        privacy_choice = get_user_choice("Select privacy:", ["Private", "Unlisted", "Public"])
        privacy_map = {1: "private", 2: "unlisted", 3: "public"}
        privacy = privacy_map[privacy_choice]
        
        # Upload
        video_id = uploader.upload(video_path, json_data, privacy=privacy)
        
        if video_id:
            print_success("Upload successful!")
            print_info(f"Video ID: {video_id}")
            print_info(f"URL: https://youtu.be/{video_id}")
            
            if privacy == "private":
                print_info(f"Review at: https://studio.youtube.com/video/{video_id}/edit")
            
            return True
        else:
            print_error("Upload failed - check your YouTube API credentials")
            return False
            
    except ImportError as e:
        print_error(f"YouTube upload module not available: {e}")
        print_info("Make sure upload_to_youtube.py exists and google-auth is installed")
        return False
    except Exception as e:
        print_error(f"Upload failed: {e}")
        return False

# ============================================
# MAIN INTERACTIVE FUNCTION
# ============================================

def estimate_duration_from_text(text):
    """Estimate video duration from text length"""
    word_count = len(text.split())
    return max(15, min(300, word_count / 2.5))

def check_dependencies():
    """Check if required packages are installed"""
    missing = []
    
    try:
        import moviepy
        print_success(f"moviepy {moviepy.__version__} found")
    except ImportError:
        missing.append("moviepy")
    
    try:
        from PIL import Image
        print_success("pillow found")
    except ImportError:
        missing.append("pillow")
    
    try:
        import gtts
        print_success("gtts found")
    except ImportError:
        missing.append("gtts")
    
    try:
        import numpy
        print_success("numpy found")
    except ImportError:
        missing.append("numpy")
    
    try:
        import google.auth
        print_success("google-auth found")
    except ImportError:
        missing.append("google-auth")
    
    if missing:
        print_warning(f"Missing dependencies: {', '.join(missing)}")
        if confirm_action("Install missing dependencies?"):
            for pkg in missing:
                print(f"   Installing {pkg}...")
                subprocess.run([sys.executable, "-m", "pip", "install", pkg])
            return True
        return False
    return True

def list_json_files():
    """List available JSON files"""
    json_files = list(Path(".").glob("*.json"))
    # Filter out client_secret.json and other non-data files
    json_files = [f for f in json_files if f.name not in ["client_secret.json", "credentials.json"]]
    return json_files

def create_sample_json():
    """Create a sample JSON file"""
    sample_data = {
        "headline": "Sample Video Headline",
        "hook_text": "Watch this amazing video! 🔥",
        "details": "This is a sample video generated for testing purposes. You can replace this with your own content.",
        "subscribe_hook": "Subscribe for more amazing content! 👍",
        "news_type": "General",
        "location": "India",
        "metadata": {
            "tags": ["sample", "test", "video"],
            "category": "Education"
        }
    }
    
    filename = "sample_data.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    print_success(f"Created sample file: {filename}")
    return Path(filename)

def main():
    """Main interactive function"""
    clear_screen()
    
    print_header("INTERACTIVE VIDEO GENERATOR")
    print("\nWelcome! This script will guide you through creating your video.")
    print("Just answer the questions and I'll handle the rest.")
    
    # Step 0: Check dependencies
    print_step("0", "Checking dependencies")
    if not check_dependencies():
        print_error("Missing dependencies. Please install them and try again.")
        input("\nPress Enter to exit...")
        return
    
    # Step 1: Select mode
    print_step("1", "Select rendering mode")
    mode_options = [
        "🏃 TEST MODE - Fast rendering (for testing)",
        "🎬 PRODUCTION MODE - High quality (for final uploads)",
        "⚡ ULTRA FAST MODE - Maximum speed (for quick tests)"
    ]
    mode_choice = get_user_choice("Choose rendering mode:", mode_options)
    
    mode_map = {1: "test", 2: "production", 3: "ultra_fast"}
    mode = mode_map[mode_choice]
    
    # Get mode description from config if available
    if CONFIG_AVAILABLE:
        from app.config import get_render_settings
        settings = get_render_settings(mode)
        print_success(f"Selected: {settings['description']}")
        print_info(f"   FPS: {settings['fps']}, Preset: {settings['preset']}, Bitrate: {settings['bitrate']}")
    else:
        print_success(f"Selected: {mode_options[mode_choice-1]}")
    
    # Step 2: Select JSON file
    print_step("2", "Select video data file")
    
    json_files = list_json_files()
    
    if not json_files:
        print_warning("No JSON data files found!")
        if confirm_action("Create a sample JSON file?"):
            json_files = [create_sample_json()]
        else:
            print_error("No JSON files available")
            input("\nPress Enter to exit...")
            return
    
    print("\nAvailable JSON files:")
    for i, file in enumerate(json_files, 1):
        size = file.stat().st_size / 1024
        modified = datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
        print(f"   {i}. {file.name} ({size:.1f} KB) - modified: {modified}")
    
    json_choice = get_user_choice("Select JSON file:", [f.name for f in json_files])
    json_file = json_files[json_choice - 1]
    
    # Load and display JSON info
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print_success(f"Loaded: {json_file.name}")
        print_info(f"   Headline: {data.get('headline', 'N/A')[:60]}...")
        print_info(f"   Type: {data.get('news_type', 'General')}")
        print_info(f"   Location: {data.get('location', 'India')}")
        
        # Estimate duration
        duration = estimate_duration_from_text(data.get('details', ''))
        print_info(f"   Estimated duration: {format_time(duration)}")
        
        # Check shorts limit
        if duration <= SHORTS_MAX_DURATION:
            print_success(f"   ✅ This will be a YouTube Short ({duration:.1f}s ≤ {SHORTS_MAX_DURATION}s)")
        else:
            print_warning(f"   ⚠️ This will be a regular video ({duration:.1f}s > {SHORTS_MAX_DURATION}s)")
        
    except Exception as e:
        print_error(f"Failed to load JSON: {e}")
        input("\nPress Enter to exit...")
        return
    
    # Step 3: Select number of images
    print_step("3", "Select number of images")
    print_info("More images = more variety, but slower processing")
    
    try:
        num_images = int(get_user_input("Number of images to fetch (2-20)", "8"))
        num_images = max(2, min(20, num_images))
    except ValueError:
        num_images = 8
    
    print_success(f"Will fetch {num_images} images")
    
    # Step 4: Upload option
    print_step("4", "YouTube upload settings")
    
    upload_choice = get_user_choice(
        "Upload to YouTube after generation?",
        ["Yes, upload automatically", "No, just generate video", "Ask me after generation"]
    )
    
    upload_option = {1: "auto", 2: "no", 3: "ask"}[upload_choice]
    
    if upload_option == "auto":
        print_success("Will auto-upload to YouTube")
    elif upload_option == "ask":
        print_info("Will ask before uploading")
    else:
        print_info("Skipping YouTube upload")
    
    # Step 5: Review and confirm
    print_step("5", "Review your selections")
    print("\n📋 SUMMARY:")
    print(f"   Mode: {mode.upper()} - {mode_options[mode_choice-1]}")
    print(f"   JSON file: {json_file.name}")
    print(f"   Images: {num_images}")
    print(f"   Duration: {format_time(duration)}")
    print(f"   Upload: {'Yes' if upload_option == 'auto' else 'Ask later' if upload_option == 'ask' else 'No'}")
    print(f"   Output folder: output/")
    
    if not confirm_action("Start video generation?"):
        print_info("Video generation cancelled.")
        input("\nPress Enter to exit...")
        return
    
    # Step 6: Generate video
    print_step("6", "Generating video")
    print_info("This may take a few minutes. Please wait...")
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Build command
    cmd = [
        sys.executable, "run_full_auto.py",
        "--json", str(json_file),
        "--images", str(num_images),
        "--mode", mode
    ]
    
    if upload_option == "no":
        cmd.append("--no-upload")
    
    # Show progress bar while running
    print("\n🎥 Rendering video...")
    
    start_time = time.time()
    pb = ProgressBar(100, prefix='   Progress:', suffix='Complete', length=40)
    
    # Run the command and capture output
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    # Simulate progress while process runs
    import threading
    import queue
    
    def enqueue_output(out, queue):
        for line in iter(out.readline, ''):
            queue.put(line)
        out.close()
    
    q = queue.Queue()
    t = threading.Thread(target=enqueue_output, args=(process.stdout, q))
    t.daemon = True
    t.start()
    
    # Update progress based on output
    progress = 0
    while True:
        try:
            line = q.get_nowait()
            print(line, end='')
            
            # Update progress based on render progress
            if "Rendering with settings" in line:
                progress = 10
            elif "Writing video" in line:
                progress = 30
            elif "Moviepy - Building video" in line:
                progress = 40
            elif "t:" in line:
                # Extract progress from moviepy output
                try:
                    import re
                    match = re.search(r't:\s*(\d+)%', line)
                    if match:
                        progress = int(match.group(1))
                except:
                    pass
            elif "RENDER COMPLETED" in line:
                progress = 100
            
            pb.update(min(progress, 100))
            
        except queue.Empty:
            if process.poll() is not None:
                break
            time.sleep(0.1)
    
    process.wait()
    total_time = time.time() - start_time
    
    # Find the latest video
    videos = list(output_dir.glob("*.mp4"))
    if videos:
        latest_video = max(videos, key=lambda p: p.stat().st_ctime)
        
        print_success("Video generated successfully!")
        print_info(f"📁 Output: {latest_video}")
        print_info(f"⏱️ Total time: {format_time(total_time)}")
        
        # Step 7: Preview video
        print_step("7", "Preview video")
        if confirm_action("Would you like to preview the video?"):
            preview_video(latest_video)
        
        # Step 8: Upload to YouTube
        print_step("8", "YouTube upload")
        
        should_upload = False
        if upload_option == "auto":
            should_upload = True
        elif upload_option == "ask":
            should_upload = confirm_action("Upload this video to YouTube?")
        
        if should_upload:
            upload_to_youtube(latest_video, data)
        else:
            print_info("Skipping YouTube upload")
    else:
        print_error("No video file found in output directory")
    
    # Final message
    print_header("THANK YOU FOR USING INTERACTIVE VIDEO GENERATOR")
    print(f"\n📁 Your video is saved in: {output_dir.absolute()}")
    print("\nOptions:")
    print("   1. Run this script again to create another video")
    print("   2. Check the output folder for your video")
    print("   3. Manually upload to YouTube if desired")
    
    input("\nPress Enter to exit...")

# ============================================
# QUICK COMMAND LINE OPTIONS
# ============================================

def quick_test():
    """Quick test mode - non-interactive"""
    print_header("QUICK TEST MODE")
    print("Running with default settings...")
    
    cmd = [sys.executable, "run_full_auto.py", "--json", "data.json", "--images", "4", "--mode", "ultra_fast"]
    subprocess.run(cmd)

def quick_prod():
    """Quick production mode - non-interactive"""
    print_header("QUICK PRODUCTION MODE")
    print("Running with production settings...")
    
    cmd = [sys.executable, "run_full_auto.py", "--json", "data.json", "--images", "8", "--mode", "production"]
    subprocess.run(cmd)

if __name__ == "__main__":
    # Check for command line arguments for non-interactive mode
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            quick_test()
        elif sys.argv[1] == "--prod":
            quick_prod()
        elif sys.argv[1] == "--help":
            print("Usage: python run_interactive.py [--test|--prod|--help]")
            print("   Without arguments: runs in interactive mode")
            print("   --test: Quick test with default settings")
            print("   --prod: Quick production run")
        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        # Default to interactive mode
        try:
            main()
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            sys.exit(0)
        except Exception as e:
            print_error(f"Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            input("\nPress Enter to exit...")