@echo off
setlocal enabledelayedexpansion
cls
echo =======================================================
echo    TrendWave Shorts HYBRID AUTOMATION (v1.3)
echo =======================================================

echo [STEP 0] Select Channel (Auto-choice in 30s)
echo 1) TrendWave Now (Cricket/Bollywood)
echo 2) SpaceMind AI (Tech/Space)
echo 3) WonderFacts24_7 (Education)
echo.

:: Set default choice by running our rotator script
for /f %%i in ('python get_next_channel.py') do set ROTATED_CH=%%i

:: Start the choice timer
choice /C 123 /T 30 /D 1 /M "Enter selection (Defaulting to %ROTATED_CH% in 30s)"
set CH_ERROR=%ERRORLEVEL%

:: If the timer actually timed out (user didn't press anything), play alert
if %CH_ERROR% EQU 1 (
    powershell -c "[console]::beep(800,200); [console]::beep(800,200)"
    set SELECTED=%ROTATED_CH%
) else if %CH_ERROR% EQU 3 (
    set SELECTED=wonderfacts
) else if %CH_ERROR% EQU 2 (
    set SELECTED=spacemind
) else (
    set SELECTED=trendwave
)

echo.
echo ?? Final Selection: %SELECTED%
echo.

:: 1. Generate the JSON via Gemini
python generate_data_json.py %SELECTED%
if %ERRORLEVEL% NEQ 0 ( echo ? JSON Gen Failed! && pause && exit /b )

:: 2. Save this choice so the NEXT run alternates correctly
python get_next_channel.py %SELECTED%

:: 3. Run the rest of your pipeline
python run_full_auto.py
python manual_image_picker.py
python run_full_auto.py --manual
python youtube_uploader.py

pause
