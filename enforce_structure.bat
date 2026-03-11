@echo off
echo ==========================================
echo Enforcing Project Structure...
echo ==========================================

echo.
echo Creating required core folders...
if not exist app mkdir app
if not exist app\audio mkdir app\audio
if not exist app\images mkdir app\images
if not exist app\video mkdir app\video
if not exist app\uploader mkdir app\uploader
if not exist tests mkdir tests

echo.
echo Creating runtime folders if missing...
if not exist audio mkdir audio
if not exist images mkdir images
if not exist logs mkdir logs
if not exist output mkdir output
if not exist temp mkdir temp

echo.
echo Moving misplaced root Python files...

if exist audio_gen.py move audio_gen.py app\audio\audio_gen.py
if exist audio_root.py move audio_root.py app\audio\audio_root.py
if exist images_root.py move images_root.py app\images\images_root.py
if exist subtitle_gen.py move subtitle_gen.py app\video\subtitle_gen.py

echo.
echo Moving root test files into tests folder...

if exist test_bollywood_images.py move test_bollywood_images.py tests\
if exist test_full_system.py move test_full_system.py tests\
if exist test_google_images.py move test_google_images.py tests\
if exist test_images_only.py move test_images_only.py tests\
if exist test_image_fetch.py move test_image_fetch.py tests\

echo.
echo Structure enforcement complete.
echo ==========================================
echo.
pause