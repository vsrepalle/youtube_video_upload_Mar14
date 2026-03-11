@echo off
setlocal enabledelayedexpansion
title 🎬 Video Generator Toolkit

:MENU
cls
echo ================================================================================
echo                          🎬 VIDEO GENERATOR TOOLKIT
echo ================================================================================
echo.
echo Welcome to the Video Generator Toolkit! This menu will guide you through
echo all available operations. Just select a number and follow the instructions.
echo.
echo ================================================================================
echo CURRENT STATUS:
echo ================================================================================

REM Check for selected images
if exist selected_images.txt (
    for /f %%i in ('type selected_images.txt ^| find /c /v ""') do set img_count=%%i
    echo 📸 Selected images: %img_count% images ready
) else (
    echo 📸 Selected images: None (will need to select or fetch)
)

REM Check for EXE
if exist dist\VideoGenerator.exe (
    echo ✅ Production EXE: Available
) else (
    echo ⚠️ Production EXE: Not built yet
)

REM Check for backup
dir /ad /b backup_* >nul 2>&1
if errorlevel 1 (
    echo 💾 Backup: None found
) else (
    echo 💾 Backup: Available
)

echo ================================================================================
echo.
echo 📋 MAIN MENU - Choose an option:
echo ================================================================================
echo.
echo [1] 🎨 SELECT IMAGES - Run image selector UI (choose which images to use)
echo     (First step - choose your images)
echo.
echo [2] 🎥 GENERATE VIDEO - Create video with selected images
echo     (Use this after selecting images)
echo.
echo [3] ⚡ DO EVERYTHING - Select images + Generate video + Upload option
echo     (Full automated workflow)
echo.
echo [4] 🏗️ BUILD EXE - Create standalone executable
echo     (Makes a portable .exe file)
echo.
echo [5] 📦 RUN PRODUCTION EXE - Use the built .exe file
echo     (Runs the compiled version)
echo.
echo [6] 📤 CREATE PORTABLE PACKAGE - Package everything for distribution
echo     (Creates a folder you can copy to any PC)
echo.
echo [7] 💾 CREATE BACKUP - Save current working version
echo     (Backup before making changes)
echo.
echo [8] 🔄 RESTORE FROM BACKUP - Revert to a previous version
echo     (If something breaks)
echo.
echo [9] ❓ HELP - Show detailed instructions
echo.
echo [0] 🚪 EXIT
echo.
echo ================================================================================
set /p choice="👉 Enter your choice (0-9): "

if "%choice%"=="1" goto SELECT_IMAGES
if "%choice%"=="2" goto GENERATE_VIDEO
if "%choice%"=="3" goto DO_EVERYTHING
if "%choice%"=="4" goto BUILD_EXE
if "%choice%"=="5" goto RUN_EXE
if "%choice%"=="6" goto PORTABLE
if "%choice%"=="7" goto BACKUP
if "%choice%"=="8" goto RESTORE
if "%choice%"=="9" goto HELP
if "%choice%"=="0" exit /b

echo ❌ Invalid choice. Press any key to try again.
pause >nul
goto MENU

:SELECT_IMAGES
cls
echo ================================================================================
echo 🎨 SELECT IMAGES
echo ================================================================================
echo.
echo This will open the image selector in your browser where you can:
echo   - View each downloaded image
echo   - Click KEEP to include in video
echo   - Click SKIP to exclude
echo   - Preview images in full size
echo   - See image details
echo.
echo ================================================================================
echo.
echo Press any key to launch the image selector...
pause >nul

python app/images/direct_image_selector.py --json data.json

echo.
echo ✅ Image selection complete!
echo.
echo 📸 Your selected images are saved in selected_images.txt
echo.
echo Next step: Choose option 2 to generate your video
echo.
pause
goto MENU

:GENERATE_VIDEO
cls
echo ================================================================================
echo 🎥 GENERATE VIDEO
echo ================================================================================
echo.

if not exist selected_images.txt (
    echo ⚠️ No selected_images.txt found!
    echo.
    echo You need to select images first (Option 1) or they will be fetched automatically.
    echo.
    set /p fetch_choice="👉 Fetch new images instead? (y/n): "
    if /i "!fetch_choice!"=="y" (
        set use_selected=
    ) else (
        pause
        goto MENU
    )
) else (
    for /f %%i in ('type selected_images.txt ^| find /c /v ""') do set img_count=%%i
    echo 📸 Found %img_count% selected images
    set use_selected=--use-selected
)

echo.
echo 🎥 Generating video...
echo This may take a few minutes depending on video length.
echo.

if defined use_selected (
    python run_full_auto.py --json data.json --images !img_count! !use_selected!
) else (
    python run_full_auto.py --json data.json --images 8
)

echo.
echo ✅ Video generation complete!
echo 📁 Check the output folder for your video
echo.
pause
goto MENU

:DO_EVERYTHING
cls
echo ================================================================================
echo ⚡ COMPLETE WORKFLOW
echo ================================================================================
echo.
echo This will:
echo   1. Run the image selector (you choose images)
echo   2. Generate video with your selected images
echo   3. Ask if you want to upload to YouTube
echo.
echo ================================================================================
echo.
pause

REM Step 1: Select images
echo.
echo 📸 STEP 1: SELECTING IMAGES
echo ================================================================================
python app/images/direct_image_selector.py --json data.json

if not exist selected_images.txt (
    echo ❌ No images selected. Aborting.
    pause
    goto MENU
)

for /f %%i in ('type selected_images.txt ^| find /c /v ""') do set img_count=%%i
echo ✅ Selected %img_count% images

REM Step 2: Generate video
echo.
echo 🎥 STEP 2: GENERATING VIDEO
echo ================================================================================
python run_full_auto.py --json data.json --images %img_count% --use-selected

REM Step 3: Ask for upload
if %errorlevel% equ 0 (
    echo.
    echo ================================================================================
    echo 📤 Video ready! Upload to YouTube?
    echo ================================================================================
    echo.
    set /p upload="👉 Upload now? (y/n): "
    if /i "!upload!"=="y" (
        echo.
        echo 🚀 Launching YouTube uploader...
        
        REM Find latest video
        for /f "delims=" %%a in ('dir output\*.mp4 /od /b') do set latest=%%a
        if defined latest (
            python upload_to_youtube.py "output\!latest!" data.json
        ) else (
            echo ❌ No video found
        )
    )
)

echo.
echo ✅ Complete workflow finished!
pause
goto MENU

:BUILD_EXE
cls
echo ================================================================================
echo 🏗️ BUILD PRODUCTION EXE
echo ================================================================================
echo.
echo This will create a standalone .exe file that doesn't need Python installed.
echo The process may take 2-5 minutes.
echo.
echo ⚠️ IMPORTANT: Make sure your code is working correctly before building!
echo.
echo ================================================================================
echo.
set /p confirm="👉 Continue with build? (y/n): "
if /i not "!confirm!"=="y" goto MENU

echo.
echo 🔍 Checking for PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo 🏗️ Building EXE...
echo.

pyinstaller --onefile ^
            --name "VideoGenerator" ^
            --add-data "app;app" ^
            --add-data "images;images" ^
            --add-data "audio;audio" ^
            --add-data "output;output" ^
            --hidden-import "PIL" ^
            --hidden-import "moviepy" ^
            --hidden-import "gtts" ^
            --hidden-import "flask" ^
            --hidden-import "requests" ^
            run_full_auto.py

if errorlevel 1 (
    echo ❌ Build failed!
) else (
    echo.
    echo ✅ EXE built successfully!
    echo 📁 Location: dist\VideoGenerator.exe
    echo.
    echo Next: You can now use Option 5 to run the EXE
)

pause
goto MENU

:RUN_EXE
cls
echo ================================================================================
echo 📦 RUN PRODUCTION EXE
echo ================================================================================
echo.

if not exist dist\VideoGenerator.exe (
    if exist VideoGenerator.exe (
        set exe_path=VideoGenerator.exe
    ) else (
        echo ❌ Production EXE not found!
        echo.
        echo Please build it first using Option 4.
        pause
        goto MENU
    )
) else (
    set exe_path=dist\VideoGenerator.exe
)

echo ✅ Found EXE: !exe_path!
echo.

if not exist data.json (
    echo ❌ data.json not found!
    pause
    goto MENU
)

if exist selected_images.txt (
    for /f %%i in ('type selected_images.txt ^| find /c /v ""') do set count=%%i
    echo 📸 Using %count% selected images
    "!exe_path!" --json data.json --images !count! --use-selected
) else (
    echo 📸 No selected images - will fetch new ones
    "!exe_path!" --json data.json --images 8
)

echo.
echo ✅ EXE execution complete!
pause
goto MENU

:PORTABLE
cls
echo ================================================================================
echo 📤 CREATE PORTABLE PACKAGE
echo ================================================================================
echo.
echo This will create a portable package you can copy to any Windows PC.
echo The package includes the EXE and all necessary files.
echo.
echo ================================================================================
echo.

if not exist dist\VideoGenerator.exe (
    echo ❌ EXE not found! Please build it first (Option 4)
    pause
    goto MENU
)

set PORTABLE_DIR=VideoGenerator_Portable

if exist !PORTABLE_DIR! rmdir /s /q !PORTABLE_DIR!
mkdir !PORTABLE_DIR!

echo 📦 Creating package in !PORTABLE_DIR!...

copy dist\VideoGenerator.exe !PORTABLE_DIR!\ >nul
echo ✅ Copied EXE

xcopy /E /I /Y app !PORTABLE_DIR!\app\ >nul
echo ✅ Copied app modules

mkdir !PORTABLE_DIR!\images 2>nul
mkdir !PORTABLE_DIR!\audio 2>nul
mkdir !PORTABLE_DIR!\output 2>nul

copy data.json !PORTABLE_DIR!\ 2>nul
copy client_secret.json !PORTABLE_DIR!\ 2>nul
copy selected_images.txt !PORTABLE_DIR!\ 2>nul
echo ✅ Copied config files

REM Create portable launcher
(
echo @echo off
echo title Video Generator Portable
echo echo ================================================================================
echo echo 🎬 Video Generator - Portable Version
echo echo ================================================================================
echo echo.
echo echo 📁 Running from: %%~dp0
echo echo.
echo if not exist data.json (
echo     echo ❌ data.json not found!
echo     pause
echo     exit /b 1
echo )
echo.
echo if exist selected_images.txt (
echo     for /f %%%%i in ('type selected_images.txt ^| find /c /v ""') do set count=%%%%i
echo     echo 📸 Using !count! selected images
echo     "%%~dp0VideoGenerator.exe" --json data.json --images !count! --use-selected
echo ) else (
echo     echo 📸 No selected images - fetching new ones
echo     "%%~dp0VideoGenerator.exe" --json data.json --images 8
echo )
echo.
echo pause
) > !PORTABLE_DIR!\run_portable.bat
echo ✅ Created launcher

REM Create README
(
echo VIDEO GENERATOR - PORTABLE PACKAGE
echo =================================
echo.
echo 📋 HOW TO USE:
echo 1. Copy this entire folder to any Windows PC
echo 2. Make sure ImageMagick is installed (https://imagemagick.org/)
echo 3. Double-click run_portable.bat
echo.
echo 📁 FOLDER CONTENTS:
echo - VideoGenerator.exe - Main program
echo - app/ - Supporting modules
echo - images/ - For downloaded images
echo - audio/ - For voiceover files
echo - output/ - Generated videos
echo - run_portable.bat - Launcher script
echo - data.json - Your video data (if present)
echo - client_secret.json - YouTube API (if present)
echo - selected_images.txt - Your image selection (if present)
echo.
echo ⚠️ REQUIREMENTS:
echo - Windows 10 or later
echo - ImageMagick installed
echo - Internet connection (for image fetching)
echo.
) > !PORTABLE_DIR!\README.txt
echo ✅ Created README

echo.
echo ✅ Portable package created in !PORTABLE_DIR! folder
echo.
echo 📦 You can now copy this folder to any Windows PC!
echo.
pause
goto MENU

:BACKUP
cls
echo ================================================================================
echo 💾 CREATE BACKUP
echo ================================================================================
echo.
echo This will create a backup of your current working version.
echo You can restore it later if something breaks.
echo.
echo ================================================================================
echo.

set BACKUP_NAME=backup_%DATE:~-4%%DATE:~4,2%%DATE:~7,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
set BACKUP_NAME=!BACKUP_NAME: =0!

echo 📁 Creating backup: !BACKUP_NAME!

mkdir !BACKUP_NAME! 2>nul

xcopy /E /I /Y app !BACKUP_NAME!\app\ >nul
xcopy /E /I /Y images !BACKUP_NAME!\images\ >nul
xcopy /E /I /Y audio !BACKUP_NAME!\audio\ >nul
copy *.py !BACKUP_NAME!\ >nul 2>nul
copy *.bat !BACKUP_NAME!\ >nul 2>nul
copy *.json !BACKUP_NAME!\ >nul 2>nul
copy *.txt !BACKUP_NAME!\ >nul 2>nul

echo ✅ Backup created: !BACKUP_NAME!
echo.
echo 📝 Backup includes all Python files, batch files, and configs
echo.
pause
goto MENU

:RESTORE
cls
echo ================================================================================
echo 🔄 RESTORE FROM BACKUP
echo ================================================================================
echo.

dir /ad /b backup_* 2>nul
if errorlevel 1 (
    echo ❌ No backups found!
    pause
    goto MENU
)

echo Available backups:
echo.
set idx=1
for /d %%i in (backup_*) do (
    echo [!idx!] %%i
    set backup_!idx!=%%i
    set /a idx+=1
)
echo.
set /p choice="👉 Enter backup number to restore: "

set SELECTED=!backup_%choice%!
if "!SELECTED!"=="" (
    echo ❌ Invalid choice
    pause
    goto MENU
)

echo.
echo ⚠️ WARNING: This will overwrite your current files!
echo.
set /p confirm="👉 Are you sure? (y/n): "
if /i not "!confirm!"=="y" goto MENU

echo.
echo 🔄 Restoring from !SELECTED!...

REM Create pre-restore backup just in case
set PRE_RESTORE=pre_restore_%DATE:~-4%%DATE:~4,2%%DATE:~7,2%_%TIME:~0,2%%TIME:~3,2%
set PRE_RESTORE=!PRE_RESTORE: =0!
mkdir !PRE_RESTORE! 2>nul
xcopy /E /I /Y app !PRE_RESTORE!\app\ >nul
xcopy /E /I /Y images !PRE_RESTORE!\images\ >nul
xcopy /E /I /Y audio !PRE_RESTORE!\audio\ >nul
copy *.py !PRE_RESTORE!\ >nul 2>nul
echo ✅ Current state backed up to !PRE_RESTORE!

REM Restore
xcopy /E /I /Y !SELECTED!\app app\ >nul
xcopy /E /I /Y !SELECTED!\images images\ >nul
xcopy /E /I /Y !SELECTED!\audio audio\ >nul
copy !SELECTED!\*.py . >nul 2>nul
copy !SELECTED!\*.bat . >nul 2>nul
copy !SELECTED!\*.json . >nul 2>nul
copy !SELECTED!\*.txt . >nul 2>nul

echo ✅ Restored from !SELECTED!
echo.
pause
goto MENU

:HELP
cls
echo ================================================================================
echo ❓ HELP - Video Generator Toolkit
echo ================================================================================
echo.
echo This toolkit helps you manage the entire video generation process.
echo.
echo 📋 WORKFLOW ORDER:
echo ================================================================================
echo.
echo 🔴 FIRST TIME SETUP:
echo  1. Option 1: SELECT IMAGES - Choose which images to use
echo  2. Option 2: GENERATE VIDEO - Create your first video
echo.
echo 🟡 REGULAR USE:
echo  1. Option 1: SELECT IMAGES (if you want new images)
echo  2. Option 2: GENERATE VIDEO
echo  3. OR use Option 3: DO EVERYTHING (combines both)
echo.
echo 🟢 PRODUCTION USE:
echo  1. Option 4: BUILD EXE - Create standalone executable
echo  2. Option 5: RUN PRODUCTION EXE - Use the compiled version
echo  3. Option 6: CREATE PORTABLE PACKAGE - For distribution
echo.
echo 🔵 SAFETY:
echo  1. Option 7: CREATE BACKUP - Before making changes
echo  2. Option 8: RESTORE FROM BACKUP - If something breaks
echo.
echo ================================================================================
echo 📌 TIPS:
echo ================================================================================
echo - Always create a backup before making major changes
echo - The EXE (Option 4) is larger but doesn't need Python installed
echo - The portable package (Option 6) can be copied to any Windows PC
echo - ImageMagick must be installed for text rendering
echo - Your selected images are saved in selected_images.txt
echo.
echo ================================================================================
pause
goto MENU