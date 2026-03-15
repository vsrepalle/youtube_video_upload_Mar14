# FullyAutomatedYoutubeVideoUploads 🚀

An end-to-end automated pipeline designed to scrape trending news, generate high-quality video shorts using MoviePy and ImageMagick, and automatically upload them to YouTube. Now featuring a **Hybrid Selection Engine** for manual image approval.

## 📺 Targeted Channels
* **TrendWave Now:** Viral Cricket and Bollywood news (Lowercase text overlays).
* **SpaceMind AI:** Gadgets, Space technology, and AI updates.

---

## ✨ Features
- **Hybrid Image Selection:** A manual picker tool to preview and choose the best images before rendering.
- **Content Library:** Automatically archives "winner" images into a structured folder (`/content_library/category/action`) for future reuse.
- **Dynamic Video Rendering:** Creates word-level overlays and scene transitions using ImageMagick.
- **Smart JSON Handling:** Robust support for UTF-8-sig to prevent PowerShell encoding errors (BOM protection).
- **Sequential Processing:** Optimized for system stability to prevent hangs during rendering.

---

## 📂 Project Structure
```text
C:.
│   do_everything.bat        <-- MAIN CONTROLLER (Runs the full chain)
│   manual_image_picker.py   <-- NEW: User-selection & Library tool
│   complete_video_workflow.py <-- Logic coordinator (Image processing)
│   run_full_auto.py         <-- Video engine (MoviePy rendering)
│   upload_to_youtube.py     <-- YouTube API uploader
├───content_library/         <-- ARCHIVE: Pre-approved images by category
├───images/
│   ├───fetched/             <-- Current project "winner" images
│   └───temp_selection/      <-- Temporary Bing search results
├───output/                  <-- Final MP4 files
└───data_trendwave.json      <-- Scene-based input data

How to Run in PowerShell
To ensure everything runs smoothly with the new manual selection step, follow this sequence:

1. Generate the News Data
Create your data_trendwave.json or data_spacemind.json.

2. Run the Manual Image Picker
This will download 5 options per scene, open them for you to view, and ask you to pick the best one.

PowerShell
python manual_image_picker.py data_trendwave.json
3. Run the Full Automation
Once you have picked your images, run the master batch file to generate audio, render the video, and upload it.

PowerShell
.\do_everything.bat
⚙️ Technical Stack
Language: Python 3.13+

Video Engine: MoviePy 2.0+ & ImageMagick 7.1.2-Q16-HDRI

Dependencies: icrawler (Bing/Google), Pillow (PIL), google-api-python-client

Automation: Windows PowerShell & Batch

📝 User Notes
Privacy: All videos are uploaded as Private by default for final review.

Hooks: "Subscribe" or "Tune with us" hooks are strictly reserved for the final scene.

System Safety: Parallel processing is disabled to prevent machine hangs during ImageMagick operations.