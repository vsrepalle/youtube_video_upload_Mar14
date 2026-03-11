@echo off
echo ========================================
echo 🎨 Web-based Image Selector
echo ========================================
echo.

REM Install requirements if needed
pip install -r requirements_ui.txt

REM Run the selector
python -m app.images.image_selector_ui --dir images/fetched --output selected_images.txt

pause