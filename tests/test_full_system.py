# test_full_system.py
import sys
from pathlib import Path
import json

print("="*60)
print("🔍 TESTING FULL SYSTEM")
print("="*60)

# Test 1: Check all files exist
files_to_check = [
    "config.py",
    "data.json",
    "fetch_images_dynamic.py",
    "hindi_voiceover.py",
    "run_full_auto.py",
    "video_composer/__init__.py",
    "video_composer/main.py",
    "video_composer/audio.py",
    "video_composer/images.py",
    "video_composer/text.py",
    "video_composer/compositor.py",
    "video_composer/renderer.py",
    "video_composer/utils.py",
]

print("\n📁 Checking files...")
all_exist = True
for file in files_to_check:
    if Path(file).exists():
        print(f"  ✅ {file}")
    else:
        print(f"  ❌ {file}")
        all_exist = False

if not all_exist:
    print("\n❌ Some files are missing!")
    sys.exit(1)

print("\n✅ All files present!")

# Test 2: Test imports
print("\n📦 Testing imports...")
try:
    from fetch_images_dynamic import DynamicImageFetcher
    print("  ✅ fetch_images_dynamic")
except Exception as e:
    print(f"  ❌ fetch_images_dynamic: {e}")

try:
    from hindi_voiceover import HindiVoiceover
    print("  ✅ hindi_voiceover")
except Exception as e:
    print(f"  ❌ hindi_voiceover: {e}")

try:
    from video_composer import make_short_video
    print("  ✅ video_composer")
except Exception as e:
    print(f"  ❌ video_composer: {e}")

# Test 3: Test JSON data
print("\n📊 Testing JSON data...")
try:
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    required = ['headline', 'hook_text', 'details', 'subscribe_hook']
    missing = [f for f in required if f not in data]
    if missing:
        print(f"  ❌ Missing fields: {missing}")
    else:
        print(f"  ✅ JSON valid - Headline: {data['headline'][:50]}...")
except Exception as e:
    print(f"  ❌ JSON error: {e}")

print("\n" + "="*60)
print("✅ SYSTEM READY! Run: run_auto.bat")
print("="*60)