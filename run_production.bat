@echo off
echo ================================================================================
echo 🎬 Video Generator - Production Version
echo ================================================================================
echo.

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0
cd /d %SCRIPT_DIR%

echo 📁 Running from: %SCRIPT_DIR%
echo.

REM Check if the EXE exists
if not exist "%SCRIPT_DIR%dist\VideoGenerator.exe" (
    if exist "%SCRIPT_DIR%VideoGenerator.exe" (
        set EXE_PATH=%SCRIPT_DIR%VideoGenerator.exe
    ) else (
        echo ❌ VideoGenerator.exe not found!
        echo.
        echo Please run build_exe.bat first to create the executable.
        pause
        exit /b 1
    )
) else (
    set EXE_PATH=%SCRIPT_DIR%dist\VideoGenerator.exe
)

REM Check for data.json
if not exist "%SCRIPT_DIR%data.json" (
    echo ❌ data.json not found!
    pause
    exit /b 1
)

REM Check for selected images
if exist "%SCRIPT_DIR%selected_images.txt" (
    echo 📸 Found selected_images.txt
    for /f %%i in ('type "%SCRIPT_DIR%selected_images.txt" ^| find /c /v ""') do set IMG_COUNT=%%i
    echo ✅ Using !IMG_COUNT! pre-selected images
) else (
    echo 📸 No selected images found - will fetch new ones
    set IMG_COUNT=8
)

echo.
echo 🚀 Launching Video Generator...
echo.

"%EXE_PATH%" --json "%SCRIPT_DIR%data.json" --images !IMG_COUNT! --use-selected

echo.
echo ✅ Video generation complete!
pause