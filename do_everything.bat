@echo off
setlocal EnableDelayedExpansion

title TrendWave Shorts - FULL AUTOMATION
echo.
echo =======================================================
echo   TrendWave Shorts FULL AUTOMATION (Fixed Input)
echo =======================================================

cd /d "%~dp0"

echo [STEP 1] Downloading images...
:: Using the --auto-download flag to bypass the interactive menu
python complete_video_workflow.py --auto-download

if %errorlevel% neq 0 (
    echo ERROR: Image download failed
    pause
    exit /b 1
)

echo.
echo [STEP 2] Creating selected_images.txt...
del /Q selected_images.txt 2>nul
(for %%F in ("images\fetched\*.jpg" "images\fetched\*.jpeg" "images\fetched\*.png" "images\fetched\*.webp") do @echo %%~fF) > selected_images.txt

echo.
echo [STEP 3] Creating video...
python run_full_auto.py --json data.json --use-selected

echo.
echo [STEP 4] Uploading latest video to YouTube...
set "latest_video="
for /f "delims=" %%f in ('dir /b /o:-d /a-d "output\*.mp4" 2^>nul') do (
    if not defined latest_video set "latest_video=%%f"
)

if defined latest_video (
    python upload_to_youtube.py "output\%latest_video%" data.json
)

echo.
echo =======================================================
echo             PROCESS COMPLETED
echo =======================================================
pause