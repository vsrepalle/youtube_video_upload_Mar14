@echo off
title TrendWave - Project Cleanup
echo =======================================================
echo          CLEANING TEMPORARY ASSETS
echo =======================================================

:: Navigate to script directory
cd /d "%~dp0"

echo [1/4] Clearing word-level scene images...
if exist "images\final_scenes" (
    del /Q "images\final_scenes\*.jpg" 2>nul
    del /Q "images\final_scenes\*.png" 2>nul
)

echo [2/4] Clearing fetched source images...
if exist "images\fetched" (
    del /Q "images\fetched\*.jpg" 2>nul
    del /Q "images\fetched\*.jpeg" 2>nul
    del /Q "images\fetched\*.png" 2>nul
    del /Q "images\fetched\*.webp" 2>nul
)

echo [3/4] Clearing temporary audio files...
if exist "temp_audio" (
    del /Q "temp_audio\*.mp3" 2>nul
)

echo [4/4] Removing temporary video fragments...
del /Q "temp_v.mp4" 2>nul
del /Q "selected_images.txt" 2>nul

echo.
echo =======================================================
echo             CLEANUP COMPLETED
echo =======================================================
timeout /t 3