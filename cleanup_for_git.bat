@echo off
echo ==========================================
echo Restructuring project files...
echo ==========================================

echo.
echo Creating target folders if not exist...
if not exist app\audio mkdir app\audio
if not exist app\images mkdir app\images
if not exist app\video mkdir app\video

echo.
echo Moving audio files...
if exist audio_gen.py move audio_gen.py app\audio\audio_gen.py
if exist audio_root.py move audio_root.py app\audio\audio_root.py

echo.
echo Moving image files...
if exist images_root.py move images_root.py app\images\images_root.py

echo.
echo Moving subtitle file...
if exist subtitle_gen.py move subtitle_gen.py app\video\subtitle_gen.py

echo.
echo ==========================================
echo Restructure completed successfully.
echo ==========================================
echo.
pause