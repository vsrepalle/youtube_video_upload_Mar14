@echo off
setlocal enabledelayedexpansion

:MENU
cls
echo ================================================================================
echo 🧹 VIDEO GENERATOR - CLEANUP UTILITY
echo ================================================================================
echo.
echo This utility helps you clean up temporary files while preserving your project.
echo Choose what you want to clean:
echo.
echo ================================================================================
echo CURRENT FOLDER STATUS:
echo ================================================================================

REM Count images
if exist images\fetched (
    dir /a-d /s images\fetched\*.jpg images\fetched\*.png images\fetched\*.webp 2>nul | find /c /v "" > temp_count.txt
    set /p img_count=<temp_count.txt
    del temp_count.txt
    if !img_count! gtr 0 (
        echo 📸 Downloaded images: !img_count! files
    ) else (
        echo 📸 Downloaded images: None
    )
) else (
    echo 📸 Downloaded images: Folder not found
)

REM Count videos
if exist output (
    dir /a-d /s output\*.mp4 2>nul | find /c /v "" > temp_count.txt
    set /p vid_count=<temp_count.txt
    del temp_count.txt
    if !vid_count! gtr 0 (
        echo 🎬 Generated videos: !vid_count! files
    ) else (
        echo 🎬 Generated videos: None
    )
) else (
    echo 🎬 Generated videos: Folder not found
)

REM Count audio files
if exist audio (
    dir /a-d /s audio\*.mp3 2>nul | find /c /v "" > temp_count.txt
    set /p aud_count=<temp_count.txt
    del temp_count.txt
    if !aud_count! gtr 0 (
        echo 🔊 Voiceover files: !aud_count! files
    ) else (
        echo 🔊 Voiceover files: None
    )
) else (
    echo 🔊 Voiceover files: Folder not found
)

echo ================================================================================
echo.
echo CLEANUP OPTIONS:
echo ================================================================================
echo.
echo [1] 🧹 Clean Downloaded Images Only
echo     (Deletes all images in images\fetched folder)
echo.
echo [2] 🎬 Clean Generated Videos Only  
echo     (Deletes all MP4 files in output folder)
echo.
echo [3] 🔇 Clean Voiceover Files Only
echo     (Deletes all MP3 files in audio folder)
echo.
echo [4] 🗑️ Clean ALL Temporary Files
echo     (Deletes images, videos, and audio files)
echo.
echo [5] 📦 Clean EXCEPT Last Video
echo     (Keeps only the most recent video, deletes everything else)
echo.
echo [6] 📝 Clean Selection File Only
echo     (Deletes selected_images.txt)
echo.
echo [7] 🔄 Reset Everything (Keep Project Structure)
echo     (Deletes ALL generated files but keeps folders)
echo.
echo [8] ❓ Show Disk Space
echo     (Display current folder sizes)
echo.
echo [9] 🚪 Exit
echo.
echo ================================================================================
set /p choice="👉 Enter your choice (1-9): "

if "%choice%"=="1" goto CLEAN_IMAGES
if "%choice%"=="2" goto CLEAN_VIDEOS
if "%choice%"=="3" goto CLEAN_AUDIO
if "%choice%"=="4" goto CLEAN_ALL
if "%choice%"=="5" goto CLEAN_EXCEPT_LAST
if "%choice%"=="6" goto CLEAN_SELECTION
if "%choice%"=="7" goto RESET_ALL
if "%choice%"=="8" goto SHOW_SPACE
if "%choice%"=="9" exit /b

echo ❌ Invalid choice. Press any key to try again.
pause >nul
goto MENU

:CLEAN_IMAGES
cls
echo ================================================================================
echo 🧹 CLEAN DOWNLOADED IMAGES
echo ================================================================================
echo.

if not exist images\fetched (
    echo 📸 No images folder found.
    pause
    goto MENU
)

dir /a-d images\fetched\*.jpg images\fetched\*.png images\fetched\*.webp 2>nul | find /c /v "" > temp_count.txt
set /p count=<temp_count.txt
del temp_count.txt

if %count% equ 0 (
    echo 📸 No images to clean.
    pause
    goto MENU
)

echo Found %count% image(s) in images\fetched
echo.
dir /b images\fetched\*.jpg images\fetched\*.png images\fetched\*.webp 2>nul
echo.

set /p confirm="👉 Delete these images? (y/n): "
if /i not "!confirm!"=="y" goto MENU

del /q images\fetched\*.jpg 2>nul
del /q images\fetched\*.png 2>nul
del /q images\fetched\*.webp 2>nul
del /q images\fetched\*.jpeg 2>nul

echo ✅ Deleted %count% image(s)
echo.
pause
goto MENU

:CLEAN_VIDEOS
cls
echo ================================================================================
echo 🎬 CLEAN GENERATED VIDEOS
echo ================================================================================
echo.

if not exist output (
    echo 📁 No output folder found.
    pause
    goto MENU
)

dir /a-d output\*.mp4 2>nul | find /c /v "" > temp_count.txt
set /p count=<temp_count.txt
del temp_count.txt

if %count% equ 0 (
    echo 🎬 No videos to clean.
    pause
    goto MENU
)

echo Found %count% video(s) in output folder
echo.
dir /b output\*.mp4 2>nul
echo.

set /p confirm="👉 Delete these videos? (y/n): "
if /i not "!confirm!"=="y" goto MENU

del /q output\*.mp4 2>nul

echo ✅ Deleted %count% video(s)
echo.
pause
goto MENU

:CLEAN_AUDIO
cls
echo ================================================================================
echo 🔇 CLEAN VOICEOVER FILES
echo ================================================================================
echo.

if not exist audio (
    echo 📁 No audio folder found.
    pause
    goto MENU
)

dir /a-d audio\*.mp3 2>nul | find /c /v "" > temp_count.txt
set /p count=<temp_count.txt
del temp_count.txt

if %count% equ 0 (
    echo 🔊 No audio files to clean.
    pause
    goto MENU
)

echo Found %count% audio file(s) in audio folder
echo.
dir /b audio\*.mp3 2>nul
echo.

set /p confirm="👉 Delete these audio files? (y/n): "
if /i not "!confirm!"=="y" goto MENU

del /q audio\*.mp3 2>nul

echo ✅ Deleted %count% audio file(s)
echo.
pause
goto MENU

:CLEAN_ALL
cls
echo ================================================================================
echo 🗑️ CLEAN ALL TEMPORARY FILES
echo ================================================================================
echo.
echo This will delete:
echo   - All downloaded images (images\fetched)
echo   - All generated videos (output)
echo   - All voiceover files (audio)
echo   - Selected images list (selected_images.txt)
echo.

set /p confirm="👉 Delete ALL temporary files? (y/n): "
if /i not "!confirm!"=="y" goto MENU

echo.
echo Cleaning images...
if exist images\fetched (
    del /q images\fetched\*.jpg 2>nul
    del /q images\fetched\*.png 2>nul
    del /q images\fetched\*.webp 2>nul
    del /q images\fetched\*.jpeg 2>nul
    echo   ✅ Images cleaned
) else (
    echo   ⚠️ No images folder
)

echo Cleaning videos...
if exist output (
    del /q output\*.mp4 2>nul
    echo   ✅ Videos cleaned
) else (
    echo   ⚠️ No output folder
)

echo Cleaning audio...
if exist audio (
    del /q audio\*.mp3 2>nul
    echo   ✅ Audio cleaned
) else (
    echo   ⚠️ No audio folder
)

echo Cleaning selection file...
if exist selected_images.txt (
    del /q selected_images.txt
    echo   ✅ Selection file cleaned
) else (
    echo   ⚠️ No selection file
)

echo.
echo ✅ All temporary files cleaned!
echo.
pause
goto MENU

:CLEAN_EXCEPT_LAST
cls
echo ================================================================================
echo 📦 CLEAN EXCEPT LAST VIDEO
echo ================================================================================
echo.
echo This will keep ONLY the most recent video and delete everything else.
echo.

if not exist output (
    echo 📁 No output folder found.
    pause
    goto MENU
)

dir /a-d output\*.mp4 2>nul | find /c /v "" > temp_count.txt
set /p count=<temp_count.txt
del temp_count.txt

if %count% equ 0 (
    echo 🎬 No videos found.
    pause
    goto MENU
)

REM Find the latest video
for /f "delims=" %%a in ('dir output\*.mp4 /od /b') do set latest=%%a

echo Current videos:
dir /b output\*.mp4 2>nul
echo.
echo 📌 Will KEEP: %latest%
echo.

set /p confirm="👉 Delete ALL other files (images, audio, other videos)? (y/n): "
if /i not "!confirm!"=="y" goto MENU

REM Delete all images
if exist images\fetched (
    del /q images\fetched\*.jpg 2>nul
    del /q images\fetched\*.png 2>nul
    del /q images\fetched\*.webp 2>nul
)

REM Delete all audio
if exist audio (
    del /q audio\*.mp3 2>nul
)

REM Delete all videos except latest
cd output
for %%f in (*.mp4) do (
    if not "%%f"=="%latest%" (
        del "%%f"
    )
)
cd ..

REM Delete selection file
if exist selected_images.txt (
    del selected_images.txt
)

echo ✅ Cleanup complete! Kept: %latest%
echo.
pause
goto MENU

:CLEAN_SELECTION
cls
echo ================================================================================
echo 📝 CLEAN SELECTION FILE ONLY
echo ================================================================================
echo.

if not exist selected_images.txt (
    echo 📝 No selection file found.
    pause
    goto MENU
)

echo Current selection file: selected_images.txt
type selected_images.txt
echo.

set /p confirm="👉 Delete this selection file? (y/n): "
if /i not "!confirm!"=="y" goto MENU

del selected_images.txt
echo ✅ Selection file deleted
echo.
pause
goto MENU

:RESET_ALL
cls
echo ================================================================================
echo 🔄 RESET EVERYTHING (Keep Project Structure)
echo ================================================================================
echo.
echo This will delete ALL generated files but keep the folder structure:
echo   - All images in images\fetched
echo   - All videos in output  
echo   - All audio files in audio
echo   - Selection file
echo   - Temporary files
echo.

set /p confirm="👉 Are you ABSOLUTELY sure? (y/n): "
if /i not "!confirm!"=="y" goto MENU

echo.
echo Cleaning images...
if exist images\fetched (
    del /q images\fetched\*.jpg 2>nul
    del /q images\fetched\*.png 2>nul
    del /q images\fetched\*.webp 2>nul
    del /q images\fetched\*.jpeg 2>nul
    echo   ✅ Images cleaned
)

echo Cleaning videos...
if exist output (
    del /q output\*.mp4 2>nul
    echo   ✅ Videos cleaned
)

echo Cleaning audio...
if exist audio (
    del /q audio\*.mp3 2>nul
    echo   ✅ Audio cleaned
)

echo Cleaning selection file...
if exist selected_images.txt (
    del selected_images.txt
    echo   ✅ Selection file cleaned
)

echo Cleaning Python cache...
if exist __pycache__ (
    rmdir /s /q __pycache__
    echo   ✅ Python cache cleaned
)

if exist app\__pycache__ (
    rmdir /s /q app\__pycache__
)

if exist app\video\__pycache__ (
    rmdir /s /q app\video\__pycache__
)

if exist app\images\__pycache__ (
    rmdir /s /q app\images\__pycache__
)

if exist app\uploader\__pycache__ (
    rmdir /s /q app\uploader\__pycache__
)

echo.
echo ✅ Project reset complete! Folder structure preserved.
echo.
pause
goto MENU

:SHOW_SPACE
cls
echo ================================================================================
echo 📊 DISK SPACE USAGE
echo ================================================================================
echo.

echo 📸 Images folder:
if exist images\fetched (
    dir /s images\fetched 2>nul | find "File(s)"
) else (
    echo   Folder not found
)

echo.
echo 🎬 Output folder:
if exist output (
    dir /s output 2>nul | find "File(s)"
) else (
    echo   Folder not found
)

echo.
echo 🔊 Audio folder:
if exist audio (
    dir /s audio 2>nul | find "File(s)"
) else (
    echo   Folder not found
)

echo.
echo 📦 Total project size:
dir /s 2>nul | find "File(s)" | find /v "Directory"

echo.
pause
goto MENU