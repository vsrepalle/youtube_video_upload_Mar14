@echo off
setlocal enabledelayedexpansion

echo =======================================================
echo    TrendWave Shorts HYBRID AUTOMATION (v1.2)
echo =======================================================

:: STEP 1: ARCHIVE OLD AND FETCH NEW OPTIONS
echo [STEP 1] Fetching 5 image options per scene...
python run_full_auto.py
if %ERRORLEVEL% NEQ 0 (echo ? Fetching failed. & pause & exit /b)

:: STEP 2: MANUAL SELECTION
echo [STEP 2] Launching Image Picker...
echo ?? Pick the best image for each scene.
python manual_image_picker.py data.json
if %ERRORLEVEL% NEQ 0 (echo ? Selection cancelled. & pause & exit /b)

:: STEP 3: CREATE VIDEO (Using --manual flag to skip re-fetching)
echo [STEP 3] Rendering Final MP4 with selected images...
python run_full_auto.py --manual
if %ERRORLEVEL% NEQ 0 (echo ? Rendering failed. & pause & exit /b)

:: STEP 4: UPLOAD
echo [STEP 4] Uploading to YouTube with Metadata...
python upload_to_youtube.py
if %ERRORLEVEL% NEQ 0 (echo ? Upload failed. & pause & exit /b)

echo =======================================================
echo          ?? PROCESS COMPLETED SUCCESSFULLY!
echo =======================================================
pause
