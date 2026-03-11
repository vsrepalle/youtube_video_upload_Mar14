@echo off
setlocal enabledelayedexpansion

echo ================================================================================
echo 📚 README FILE CREATOR
echo ================================================================================
echo.
echo This will create comprehensive README files for your project.
echo.

REM Create README folder
if not exist READMEs mkdir READMEs
echo ✅ Created READMEs folder
echo.

REM ================================================================================
REM FUNCTIONAL README - For end users
REM ================================================================================
echo Creating FUNCTIONAL_README.md (for end users)...

(
echo # 🎬 Video Generator - User Guide
echo.
echo ![Version](https://img.shields.io/badge/version-2.0-blue)
echo ![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
echo ![Python](https://img.shields.io/badge/python-3.8%2B-green)
echo.
echo Welcome to the **Video Generator** – your all-in-one tool for creating professional YouTube Shorts and videos automatically! This guide will help you get started quickly.
echo.
echo ---
echo.
echo ## 📋 Table of Contents
echo.
echo 1. [What This Tool Does](#what-this-tool-does)
echo 2. [Quick Start](#quick-start)
echo 3. [Step-by-Step Workflow](#step-by-step-workflow)
echo 4. [Creating Your First Video](#creating-your-first-video)
echo 5. [Understanding the Output](#understanding-the-output)
echo 6. [Troubleshooting](#troubleshooting)
echo.
echo ---
echo.
echo ## 🎯 What This Tool Does
echo.
echo This tool automatically:
echo - 📸 **Fetches relevant images** based on your news topic
echo - 🔍 **Lets you select images** through a web interface
echo - 🔊 **Creates Hindi voiceover** from your text
echo - 🎬 **Generates vertical videos** perfect for YouTube Shorts
echo - 📤 **Uploads to YouTube** (optional)
echo.
echo ---
echo.
echo ## ⚡ Quick Start
echo.
echo ### Prerequisites
echo.
echo 1. **Windows 10 or 11**
echo 2. **ImageMagick** installed ([Download here](https://imagemagick.org/))
echo 3. **Python 3.8+** (if running from source)
echo 4. **Internet connection** (for image fetching)
echo.
echo ### One-Command Workflow
echo.
echo Just double-click:
echo ```batch
echo VideoGenerator_Toolkit.bat
echo ```
echo.
echo Then select option **3** from the menu – it does everything automatically!
echo.
echo ---
echo.
echo ## 📝 Step-by-Step Workflow
echo.
echo ### Step 1: Prepare Your Data
echo.
echo Create a `data.json` file with your content:
echo.
echo ```json
echo {
echo   "headline": "Your Video Headline",
echo   "hook_text": "Attention-grabbing hook",
echo   "details": "Full story text here...",
echo   "subscribe_hook": "Subscribe message",
echo   "news_type": "Sports/Bollywood/News",
echo   "location": "Mumbai, India",
echo   "image_search_keys": [
echo     "search term 1",
echo     "search term 2"
echo   ]
echo }
echo ```
echo.
echo ### Step 2: Select Images
echo.
echo ```batch
echo # Run the image selector
echo python app/images/direct_image_selector.py --json data.json
echo ```
echo.
echo This opens a browser where you can:
echo - ✅ Click KEEP to include images
echo - ❌ Click SKIP to exclude
echo - 👁️ Preview images in full size
echo.
echo ### Step 3: Generate Video
echo.
echo ```batch
echo # Generate with selected images
echo python run_full_auto.py --json data.json --images 8 --use-selected
echo ```
echo.
echo ### Step 4: Upload to YouTube (Optional)
echo.
echo ```batch
echo # Upload the latest video
echo python upload_to_youtube.py --latest
echo ```
echo.
echo ---
echo.
echo ## 🎬 Creating Your First Video
echo.
echo ### Method 1: Using the Toolkit Menu (Easiest)
echo.
echo 1. Double-click `VideoGenerator_Toolkit.bat`
echo 2. Choose option **1** to select images
echo 3. In the browser, click KEEP/SKIP for each image
echo 4. Close the browser and return to the menu
echo 5. Choose option **2** to generate video
echo 6. Wait for rendering to complete
echo 7. Find your video in the `output` folder
echo.
echo ### Method 2: All-in-One (Fastest)
echo.
echo 1. Double-click `VideoGenerator_Toolkit.bat`
echo 2. Choose option **3** (DO EVERYTHING)
echo 3. The tool will:
echo    - Open image selector
echo    - Wait for your selections
echo    - Generate video automatically
echo    - Ask about YouTube upload
echo.
echo ---
echo.
echo ## 📁 Understanding the Output
echo.
echo ### Folder Structure
echo.
echo ```
echo your-project/
echo ├── output/           # Your videos are saved here
echo │   └── *.mp4
echo ├── images/fetched/   # Downloaded images
echo ├── audio/            # Voiceover files
echo ├── selected_images.txt # Your image choices
echo └── data.json         # Your content
echo ```
echo.
echo ### File Naming
echo.
echo Videos are named automatically:  
echo `Headline_YYYYMMDD_HHMMSS.mp4`
echo.
echo ---
echo.
echo ## ❓ Troubleshooting
echo.
echo | Problem | Solution |
echo |---------|----------|
echo | **No images download** | Check internet connection and search terms |
echo | **Text not showing** | Install ImageMagick |
echo | **Slow rendering** | Use TEST mode or lower quality settings |
echo | **Upload fails** | Check client_secret.json and authentication |
echo | **Black screen in video** | Images are looping – this is normal during render |
echo.
echo ### Common Error Messages
echo.
echo **"ImageMagick not found"**  
echo → Download and install from [imagemagick.org](https://imagemagick.org/)
echo.
echo **"No module named '...'"**  
echo → Run `pip install -r requirements.txt`
echo.
echo ---
echo.
echo ## 📞 Support
echo.
echo For issues, check the troubleshooting section above or re-run with `--debug` flag.
echo.
echo ---
echo.
echo *Happy Video Creating!* 🎉
) > READMEs\FUNCTIONAL_README.md

echo ✅ Created FUNCTIONAL_README.md
echo.

REM ================================================================================
REM TECHNICAL README - For developers
REM ================================================================================
echo Creating TECHNICAL_README.md (for developers)...

(
echo # 🔧 Video Generator - Technical Documentation
echo.
echo ![Version](https://img.shields.io/badge/version-2.0-blue)
echo ![Python](https://img.shields.io/badge/python-3.8%2B-green)
echo ![License](https://img.shields.io/badge/license-MIT-orange)
echo.
echo This document provides technical details for developers who want to understand, modify, or extend the Video Generator system.
echo.
echo ---
echo.
echo ## 📋 Table of Contents
echo.
echo 1. [System Architecture](#system-architecture)
echo 2. [Module Structure](#module-structure)
echo 3. [Core Components](#core-components)
echo 4. [Data Flow](#data-flow)
echo 5. [Configuration Guide](#configuration-guide)
echo 6. [API Reference](#api-reference)
echo 7. [Extending the System](#extending-the-system)
echo 8. [Performance Optimization](#performance-optimization)
echo 9. [Deployment](#deployment)
echo.
echo ---
echo.
echo ## 🏗️ System Architecture
echo.
echo ```mermaid
echo graph TD
echo     A[JSON Input] --> B[Image Fetcher]
echo     A --> C[Voiceover Generator]
echo     B --> D[Image Selector UI]
echo     D --> E[Selected Images]
echo     C --> F[Audio File]
echo     E --> G[Video Composer]
echo     F --> G
echo     G --> H[Renderer]
echo     H --> I[Output MP4]
echo     I --> J[YouTube Uploader]
echo ```
echo.
echo ### Technology Stack
echo.
echo - **Python 3.8+** - Core language
echo - **MoviePy** - Video editing and rendering
echo - **Flask** - Web UI for image selection
echo - **Pillow** - Image processing
echo - **gTTS** - Hindi text-to-speech
echo - **Google APIs** - YouTube upload
echo - **PyInstaller** - EXE creation
echo.
echo ---
echo.
echo ## 📁 Module Structure
echo.
echo ```
echo app/
echo ├── __init__.py
echo ├── config.py                 # Master configuration
echo ├── video/
echo │   ├── main_video.py        # Main composition logic
echo │   ├── images_root.py       # Image processing with looping
echo │   ├── compositor.py        # Text overlay management
echo │   ├── renderer.py          # FFmpeg rendering
echo │   ├── audio.py             # Audio handling
echo │   └── text.py              # Text generation with caching
echo ├── images/
echo │   ├── fetch_images_dynamic.py  # Image downloading
echo │   ├── direct_image_selector.py # Web UI selector
echo │   └── interactive_image_selector.py # Terminal selector
echo ├── audio/
echo │   └── voice_generator.py   # Hindi voiceover
echo └── uploader/
echo     └── youtube_uploader.py  # YouTube API integration
echo ```
echo.
echo ---
echo.
echo ## 🔧 Core Components
echo.
echo ### 1. Configuration System (`config.py`)
echo.
echo The central configuration file controls all aspects:
echo.
echo ```python
echo # Key configuration sections
echo VIDEO_WIDTH = 1080           # Resolution
echo VIDEO_HEIGHT = 1920
echo MODE = "test"                # test/production/ultra_fast
echo IMAGE_DISPLAY_DURATION = 3.5 # Seconds per image
echo TRANSITION_ENABLED = True
echo ```
echo.
echo ### 2. Image Processor (`images_root.py`)
echo.
echo The image processor handles:
echo - Image loading and resizing
echo - Automatic looping to fill duration
echo - Crossfade transitions
echo.
echo ```python
echo # Smart looping algorithm
echo segments_needed = int(target_duration / base_duration) + 1
echo repeated_images = [images[i %% num_original] for i in range(segments_needed)]
echo exact_duration = target_duration / segments_needed
echo ```
echo.
echo ### 3. Video Composer (`main_video.py`)
echo.
echo Orchestrates the entire video creation process:
echo 1. Load audio and determine duration
echo 2. Process images with looping
echo 3. Add text overlays
echo 4. Compose final video
echo 5. Render with progress tracking
echo.
echo ### 4. Renderer (`renderer.py`)
echo.
echo Handles FFmpeg encoding with mode-based settings:
echo.
echo ```python
echo TEST_SETTINGS = {
echo     "fps": 20,
echo     "preset": "ultrafast",
echo     "crf": 35,
echo     "bitrate": "1000k"
echo }
echo ```
echo.
echo ---
echo.
echo ## 📊 Data Flow
echo.
echo ### JSON Input Format
echo.
echo ```json
echo {
echo   "headline": "Video Title",
echo   "hook_text": "Opening hook",
echo   "details": "Full story text",
echo   "subscribe_hook": "CTA message",
echo   "news_type": "Category",
echo   "location": "Place",
echo   "image_search_keys": ["term1", "term2"]
echo }
echo ```
echo.
echo ### Processing Pipeline
echo.
echo 1. **Image Fetching** → Downloads images for each search key
echo 2. **Image Selection** → User selects keep/skip via web UI
echo 3. **Voiceover Generation** → Text → Hindi audio
echo 4. **Image Looping** → Calculates segments to fill duration
echo 5. **Video Composition** → Combines all elements
echo 6. **Rendering** → FFmpeg encoding
echo 7. **YouTube Upload** → Optional upload
echo.
echo ---
echo.
echo ## ⚙️ Configuration Guide
echo.
echo ### Rendering Modes
echo.
echo | Mode | FPS | Preset | CRF | Bitrate | Use Case |
echo |------|-----|--------|-----|---------|----------|
echo | test | 20 | ultrafast | 35 | 1000k | Quick testing |
echo | production | 30 | faster | 23 | 5000k | Final videos |
echo | ultra_fast | 15 | ultrafast | 45 | 500k | Maximum speed |
echo.
echo ### Image Settings
echo.
echo ```python
echo IMAGE_FIT_MODE = "cover"     # "cover" or "contain"
echo IMAGE_DISPLAY_DURATION = 3.5  # Seconds per image segment
echo TRANSITION_ENABLED = True      # Crossfade between images
echo TRANSITION_DURATION = 0.5      # Fade duration
echo ```
echo.
echo ### Text Settings
echo.
echo ```python
echo HEADER_FONT_SIZE = 85         # Headline size
echo SUBTITLE_FONT_SIZE = 70       # Subtitle size
echo SUBTITLE_Y_POSITION = 1650    # Position from top
echo ```
echo.
echo ---
echo.
echo ## 📚 API Reference
echo.
echo ### Main Functions
echo.
echo ```python
echo # Core video creation
echo def make_short_video(images, audio_path, english_text, 
echo                       headline, hook, subscribe_hook, output_path):
echo     """Create video with given parameters"""
echo
echo # Image selection
echo def select_images_ui(image_paths, output_file="selected_images.txt"):
echo     """Launch web UI for image selection"""
echo
echo # YouTube upload
echo def upload_video(video_path, data, privacy="private"):
echo     """Upload to YouTube"""
echo ```
echo.
echo ### Command Line Interfaces
echo.
echo ```bash
echo # Image selector
echo python -m app.images.direct_image_selector --json data.json
echo
echo # Video generator
echo python run_full_auto.py --json data.json --images 8 --use-selected
echo
echo # YouTube upload
echo python upload_to_youtube.py output/video.mp4 data.json
echo ```
echo.
echo ---
echo.
echo ## 🚀 Extending the System
echo.
echo ### Adding New News Types
echo.
echo 1. Update `image_search_keys` generation in `fetch_images_dynamic.py`
echo 2. Add new category to `news_type` in JSON
echo 3. Update default tags in `config.py`
echo.
echo ### Custom Video Effects
echo.
echo To add new visual effects, modify `images_root.py`:
echo.
echo ```python
echo def apply_custom_effect(self, clip, duration):
echo     """Add your custom effect here"""
echo     # Example: slow zoom
echo     return clip.resize(lambda t: 1 + 0.1 * (t / duration))
echo ```
echo.
echo ### Adding New Output Formats
echo.
echo Modify `config.py` to support different resolutions:
echo.
echo ```python
echo # For horizontal videos
echo VIDEO_WIDTH = 1920
echo VIDEO_HEIGHT = 1080
echo ```
echo.
echo ---
echo.
echo ## ⚡ Performance Optimization
echo.
echo ### Speed Factors
echo.
echo | Factor | Impact | Optimization |
echo |--------|--------|--------------|
echo | Resolution | 4x slower at 4K | Use 1080p or lower for testing |
echo | FPS | 2x slower at 60fps | 20-30fps is sufficient |
echo | Bitrate | Larger files | 1000k-5000k is optimal |
echo | Image count | More images = more segments | 8-12 images is ideal |
echo.
echo ### Profiling
echo.
echo Enable detailed timing:
echo ```python
echo LOG_PERFORMANCE = True  # in config.py
echo ```
echo.
echo ---
echo.
echo ## 📦 Deployment
echo.
echo ### Creating Standalone EXE
echo.
echo ```batch
echo # From the toolkit menu
echo Option 4: BUILD EXE
echo
echo # Or manually
echo pyinstaller --onefile --name "VideoGenerator" run_full_auto.py
echo ```
echo.
echo ### Portable Package
echo.
echo ```batch
echo # From the toolkit menu
echo Option 6: CREATE PORTABLE PACKAGE
echo
echo # Creates folder with everything needed
echo ```
echo.
echo ### Distribution Requirements
echo.
echo - Windows 10/11
echo - ImageMagick installed
echo - Internet connection for image fetching
echo - YouTube API credentials (for upload)
echo.
echo ---
echo.
echo ## 🔍 Debugging
echo.
echo Enable verbose output:
echo ```python
echo DEBUG_MODE = True
echo VERBOSE_OUTPUT = True
echo ```
echo.
echo Check logs:
echo ```bash
echo # View rendering logs
echo python run_full_auto.py --json data.json --debug
echo ```
echo.
echo ---
echo.
echo ## 📝 License
echo.
echo MIT License - Free for personal and commercial use.
echo.
echo ---
echo.
echo *For questions or contributions, please refer to the FUNCTIONAL_README.md for user guide.*
) > READMEs\TECHNICAL_README.md

echo ✅ Created TECHNICAL_README.md
echo.

REM ================================================================================
REM BATCH FILES README - For running the system
REM ================================================================================
echo Creating BATCH_README.md (for running the system)...

(
echo # 🏃 Video Generator - Batch Files Guide
echo.
echo ![Version](https://img.shields.io/badge/version-2.0-blue)
echo ![Platform](https://img.shields.io/badge/platform-Windows-brightgreen)
echo.
echo This guide explains all the batch files available in the Video Generator system and how to use them.
echo.
echo ---
echo.
echo ## 📋 Table of Contents
echo.
echo 1. [Main Toolkit](#main-toolkit-videogenerator_toolkitbat)
echo 2. [Quick Start Files](#quick-start-files)
echo 3. [Build & Package Files](#build--package-files)
echo 4. [Workflow Files](#workflow-files)
echo 5. [Utility Files](#utility-files)
echo 6. [File Comparison](#file-comparison)
echo 7. [Recommended Workflow](#recommended-workflow)
echo.
echo ---
echo.
echo ## 🎯 Main Toolkit: `VideoGenerator_Toolkit.bat`
echo.
echo **This is the ONLY file you need to remember!**
echo.
echo ```batch
echo # Just double-click this file
echo VideoGenerator_Toolkit.bat
echo ```
echo.
echo ### What it does:
echo - Presents a clear menu with 9 options
echo - Shows current status (selected images, EXE availability)
echo - Guides you through each step
echo - Handles everything from image selection to YouTube upload
echo.
echo ### Menu Options:
echo.
echo | Option | Description |
echo |--------|-------------|
echo | **1** | 🎨 SELECT IMAGES - Run image selector UI |
echo | **2** | 🎥 GENERATE VIDEO - Create video with selected images |
echo | **3** | ⚡ DO EVERYTHING - Full automated workflow |
echo | **4** | 🏗️ BUILD EXE - Create standalone executable |
echo | **5** | 📦 RUN PRODUCTION EXE - Use the compiled version |
echo | **6** | 📤 CREATE PORTABLE PACKAGE - For distribution |
echo | **7** | 💾 CREATE BACKUP - Save current version |
echo | **8** | 🔄 RESTORE FROM BACKUP - Revert if needed |
echo | **9** | ❓ HELP - Show instructions |
echo | **0** | 🚪 EXIT |
echo.
echo ---
echo.
echo ## ⚡ Quick Start Files
echo.
echo ### `run_full_auto.py` (Python, not batch)
echo.
echo ```batch
echo python run_full_auto.py --json data.json --images 8 --use-selected
echo ```
echo.
echo **Purpose:** Main video generator script
echo **When to use:** When you want to run directly without the menu
echo.
echo ### `run_interactive.py` (Python, not batch)
echo.
echo ```batch
echo python run_interactive.py
echo ```
echo.
echo **Purpose:** Interactive command-line interface
echo **When to use:** When you prefer text-based menus
echo.
echo ---
echo.
echo ## 🏗️ Build & Package Files
echo.
echo ### `build_exe.bat`
echo.
echo ```batch
echo build_exe.bat
echo ```
echo.
echo **Purpose:** Creates standalone EXE using PyInstaller
echo **Output:** `dist\VideoGenerator.exe`
echo **When to use:** Before distributing or for production use
echo.
echo ### `build_simple.bat`
echo.
echo ```batch
echo build_simple.bat
echo ```
echo.
echo **Purpose:** Simpler version of EXE builder
echo **Output:** `dist\VideoGen.exe`
echo **When to use:** For quick EXE creation with fewer dependencies
echo.
echo ### `portable_package.bat`
echo.
echo ```batch
echo portable_package.bat
echo ```
echo.
echo **Purpose:** Creates a portable folder with everything needed
echo **Output:** `VideoGenerator_Portable\` folder
echo **When to use:** When you want to copy to another PC
echo.
echo ---
echo.
echo ## 🔄 Workflow Files
echo.
echo ### `do_everything.bat`
echo.
echo ```batch
echo do_everything.bat
echo ```
echo.
echo **Purpose:** Complete workflow: select images → generate video → ask for upload
echo **When to use:** When you want a one-command solution
echo.
echo ### `create_video.bat`
echo.
echo ```batch
echo create_video.bat
echo ```
echo.
echo **Purpose:** Simple video creation with selected images
echo **When to use:** After you've already selected images
echo.
echo ### `quick_video.bat`
echo.
echo ```batch
echo quick_video.bat
echo ```
echo.
echo **Purpose:** Fast video generation with existing selection
echo **When to use:** When you have images ready and want quick results
echo.
echo ### `run_production.bat`
echo.
echo ```batch
echo run_production.bat
echo ```
echo.
echo **Purpose:** Run the compiled EXE version
echo **When to use:** After building EXE, for production use
echo.
echo ---
echo.
echo ## 🛠️ Utility Files
echo.
echo ### `create_readmes.bat`
echo.
echo ```batch
echo create_readmes.bat
echo ```
echo.
echo **Purpose:** Creates all documentation files
echo **Output:** READMEs\ folder with three guides
echo **When to use:** First time setup or when you need documentation
echo.
echo ### `restore_backup.bat`
echo.
echo ```batch
echo restore_backup.bat
echo ```
echo.
echo **Purpose:** Restore from a backup if something breaks
echo **When to use:** After running `build_exe.bat` and something went wrong
echo.
echo ### `run_image_selector.bat`
echo.
echo ```batch
echo run_image_selector.bat
echo ```
echo.
echo **Purpose:** Just run the image selector UI
echo **When to use:** When you only want to select images without generating video
echo.
echo ### `run_with_zoom.bat`
echo.
echo ```batch
echo run_with_zoom.bat
echo ```
echo.
echo **Purpose:** Generate video with zoom effects enabled
echo **When to use:** When you want the Ken Burns effect on images
echo.
echo ### `run_with_selection.bat`
echo.
echo ```batch
echo run_with_selection.bat
echo ```
echo.
echo **Purpose:** Generate video with interactive image selection
echo **When to use:** When you want to select images during the process
echo.
echo ---
echo.
echo ## 📊 File Comparison
echo.
echo | File | Complexity | Use Case |
echo |------|------------|----------|
echo | `VideoGenerator_Toolkit.bat` | Low | **EVERYTHING** - One file to rule them all |
echo | `do_everything.bat` | Medium | Complete workflow in one go |
echo | `create_video.bat` | Low | Just generate video |
echo | `build_exe.bat` | High | Create production EXE |
echo | `portable_package.bat` | Medium | Create distributable package |
echo.
echo ---
echo.
echo ## 🎯 Recommended Workflow
echo.
echo ### For Beginners:
echo.
echo ```batch
echo 1. Double-click VideoGenerator_Toolkit.bat
echo 2. Choose option 1 (Select Images)
echo 3. Choose option 2 (Generate Video)
echo ```
echo.
echo ### For Regular Users:
echo.
echo ```batch
echo 1. Double-click VideoGenerator_Toolkit.bat
echo 2. Choose option 3 (Do Everything)
echo ```
echo.
echo ### For Production:
echo.
echo ```batch
echo 1. build_exe.bat
echo 2. portable_package.bat
echo 3. Copy portable_package to target PC
echo 4. Double-click run_portable.bat
echo ```
echo.
echo ### For Testing:
echo.
echo ```batch
echo 1. quick_video.bat  # If images are selected
echo 2. OR run_with_zoom.bat  # To test zoom effects
echo ```
echo.
echo ---
echo.
echo ## ❓ Frequently Asked Questions
echo.
echo ### Q: Which file should I use?
echo.
echo **A:** Always start with `VideoGenerator_Toolkit.bat` - it has a menu that guides you.
echo.
echo ### Q: Do I need to remember all these files?
echo.
echo **A:** No! Just remember `VideoGenerator_Toolkit.bat`. It can do everything.
echo.
echo ### Q: What if I want the fastest workflow?
echo.
echo **A:** Use `do_everything.bat` - it's one command for the complete process.
echo.
echo ### Q: How do I create a portable version?
echo.
echo **A:** Run `portable_package.bat` after building the EXE with `build_exe.bat`.
echo.
echo ### Q: What if something breaks?
echo.
echo **A:** Run `restore_backup.bat` to revert to a working version.
echo.
echo ---
echo.
echo ## 📝 Summary
echo.
echo | File | Purpose |
echo |------|---------|
echo | **VideoGenerator_Toolkit.bat** | **MASTER CONTROLLER** - Use this for everything |
echo | do_everything.bat | Complete workflow in one go |
echo | build_exe.bat | Create standalone EXE |
echo | portable_package.bat | Create distributable package |
echo | restore_backup.bat | Revert if something breaks |
echo | create_video.bat | Quick video generation |
echo.
echo ---
echo.
echo *Remember: When in doubt, run `VideoGenerator_Toolkit.bat`!* 🎉
) > READMEs\BATCH_README.md

echo ✅ Created BATCH_README.md
echo.

REM Create a master index file
echo Creating README.md (master index)...

(
echo # 🎬 Video Generator - Documentation Master Index
echo.
echo ![Version](https://img.shields.io/badge/version-2.0-blue)
echo ![Docs](https://img.shields.io/badge/docs-complete-green)
echo.
echo Welcome to the Video Generator documentation! This is your central hub for all guides and references.
echo.
echo ---
echo.
echo ## 📚 Available Documentation
echo.
echo ### 👤 For Users
echo.
echo | Guide | Description | When to Read |
echo |-------|-------------|--------------|
echo | **[FUNCTIONAL_README.md](FUNCTIONAL_README.md)** | End-user guide with workflows | First time users |
echo | **[BATCH_README.md](BATCH_README.md)** | Guide to all batch files | When running the system |
echo.
echo ### 🔧 For Developers
echo.
echo | Guide | Description | When to Read |
echo |-------|-------------|--------------|
echo | **[TECHNICAL_README.md](TECHNICAL_README.md)** | Architecture, APIs, extending | When modifying code |
echo.
echo ---
echo.
echo ## 🚀 Quick Links
echo.
echo - [Start Here - User Guide](FUNCTIONAL_README.md)
echo - [Batch Files Explained](BATCH_README.md)
echo - [Developer Documentation](TECHNICAL_README.md)
echo.
echo ---
echo.
echo ## 🎯 Recommended Reading Order
echo.
echo 1. **FUNCTIONAL_README.md** - Understand what the tool does
echo 2. **BATCH_README.md** - Learn how to run it
echo 3. **TECHNICAL_README.md** - Dive into code (developers only)
echo.
echo ---
echo.
echo *All documentation created on %DATE%*
) > READMEs\README.md

echo ✅ Created README.md (master index)
echo.

REM Create a summary file
echo Creating SUMMARY.txt...

(
echo ================================================================================
echo VIDEO GENERATOR - DOCUMENTATION SUMMARY
echo ================================================================================
echo.
echo 📁 All documentation has been created in the READMEs folder:
echo.
echo 📄 README.md              - Master index (start here)
echo 📄 FUNCTIONAL_README.md   - User guide with workflows
echo 📄 TECHNICAL_README.md    - Developer documentation
echo 📄 BATCH_README.md        - Guide to all batch files
echo.
echo ================================================================================
echo NEXT STEPS:
echo ================================================================================
echo.
echo 1. Open READMEs\README.md to start reading
echo 2. For first-time users, read FUNCTIONAL_README.md first
echo 3. To run the system, use VideoGenerator_Toolkit.bat
echo.
echo ================================================================================
echo DOCUMENTATION CREATED: %DATE% at %TIME%
echo ================================================================================
) > READMEs\SUMMARY.txt

echo ✅ Created SUMMARY.txt
echo.

echo ================================================================================
echo ✅ ALL README FILES CREATED SUCCESSFULLY!
echo ================================================================================
echo.
echo 📁 Location: .\READMEs\
echo.
echo Files created:
echo   1. README.md              - Master index
echo   2. FUNCTIONAL_README.md   - User guide
echo   3. TECHNICAL_README.md    - Developer guide
echo   4. BATCH_README.md        - Batch files guide
echo   5. SUMMARY.txt            - Quick summary
echo.
echo ================================================================================
echo NEXT STEPS:
echo ================================================================================
echo.
echo 1. Open READMEs\README.md to start reading
echo 2. For users: Read FUNCTIONAL_README.md
echo 3. For developers: Read TECHNICAL_README.md
echo 4. For batch files: Read BATCH_README.md
echo.
echo ================================================================================
pause