@echo off
echo ================================================================================
echo 🎬 COMPLETE IMAGE SELECTION + SENTENCE MATCHING WORKFLOW
echo ================================================================================
echo.

REM Step 1: Download and select images
echo 📸 STEP 1: Downloading and selecting images...
echo This will open a browser for you to select images.
echo.
python app/images/direct_image_selector.py --json data.json

REM Step 2: Check if images were downloaded
if not exist images\fetched\*.jpg (
    if not exist images\fetched\*.png (
        echo.
        echo ❌ No images were downloaded. Exiting.
        pause
        exit /b
    )
)

REM Step 3: Run the sentence matcher
echo.
echo 📝 STEP 2: Running sentence-image matcher...
echo.
python app/images/sentence_image_matcher.py --json data.json

pause