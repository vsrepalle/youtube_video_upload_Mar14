# fixed_debug.py
"""
Fixed debug script to check what files are being loaded
"""

import json
from pathlib import Path
from datetime import datetime

print("="*70)
print("🔍 FIXED UI DEBUGGER - Checking what files are being loaded")
print("="*70)

# Get current directory
current_dir = Path.cwd()
print(f"\n📁 Current directory: {current_dir}")
print(f"   Path exists: {current_dir.exists()}")

# Check for data.json
data_file = current_dir / "data.json"
print(f"\n📄 data.json exists: {data_file.exists()}")
if data_file.exists():
    print(f"   Size: {data_file.stat().st_size} bytes")
    print(f"   Modified: {datetime.fromtimestamp(data_file.stat().st_mtime)}")

# Check for selected_images.txt
selected_file = current_dir / "selected_images.txt"
print(f"\n📄 selected_images.txt exists: {selected_file.exists()}")
if selected_file.exists():
    print(f"   Size: {selected_file.stat().st_size} bytes")
    print(f"   Modified: {datetime.fromtimestamp(selected_file.stat().st_mtime)}")
    print("\n   Content (first 5 lines):")
    with open(selected_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines[:5]):
            print(f"     {i+1}. {line.strip()}")
        if len(lines) > 5:
            print(f"     ... and {len(lines)-5} more")

# Check for sentence_mapping.txt
mapping_file = current_dir / "sentence_mapping.txt"
print(f"\n📄 sentence_mapping.txt exists: {mapping_file.exists()}")
if mapping_file.exists():
    print(f"   Size: {mapping_file.stat().st_size} bytes")
    print(f"   Modified: {datetime.fromtimestamp(mapping_file.stat().st_mtime)}")

# Check images folder
images_dir = current_dir / "images" / "fetched"
print(f"\n📸 images/fetched exists: {images_dir.exists()}")
if images_dir.exists():
    images = list(images_dir.glob("*.*"))
    print(f"   Total files: {len(images)}")
    if images:
        print("\n   First 10 images:")
        for i, img in enumerate(images[:10]):
            size = img.stat().st_size / 1024
            mod_time = datetime.fromtimestamp(img.stat().st_mtime).strftime('%H:%M:%S')
            print(f"     {i+1}. {img.name} ({size:.1f} KB, modified: {mod_time})")
        if len(images) > 10:
            print(f"     ... and {len(images)-10} more")
    else:
        print("   📂 Folder is empty")
else:
    print("   📂 Folder does not exist")

# Check for any other txt files
print(f"\n📋 All .txt files in current directory:")
txt_files = list(current_dir.glob("*.txt"))
if txt_files:
    for txt in txt_files:
        size = txt.stat().st_size / 1024
        mod_time = datetime.fromtimestamp(txt.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        print(f"   - {txt.name} ({size:.1f} KB, modified: {mod_time})")
else:
    print("   No .txt files found")

# Check for any pycache folders (cached data)
cache_dirs = [
    current_dir / "__pycache__",
    current_dir / "app" / "__pycache__",
    current_dir / "app" / "images" / "__pycache__",
    current_dir / "app" / "video" / "__pycache__",
]

print(f"\n🗑️ Checking cache directories:")
for cache in cache_dirs:
    if cache.exists():
        size = sum(f.stat().st_size for f in cache.glob("**/*") if f.is_file()) / 1024
        print(f"   ⚠️ {cache} exists ({size:.1f} KB) - may contain cached data")
    else:
        print(f"   ✅ {cache} not found")

print("\n" + "="*70)
print("✅ Debug check complete!")
print("="*70)