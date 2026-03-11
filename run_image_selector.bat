@echo off
echo ========================================
echo 🎨 Direct Image Selector
echo ========================================
echo.

REM Install requirements if needed
pip install flask pillow requests

REM Run the selector
python -m app.images.direct_image_selector --json data.json --output selected_images.txt

pause