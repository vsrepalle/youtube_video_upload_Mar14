@echo off
setlocal EnableDelayedExpansion

echo ============================================
echo      GIT PUSH TO REMOTE REPOSITORY
echo ============================================

cd /d %~dp0

if not exist ".git" (
    echo [INFO] Initializing Git Repository...
    git init
)

:: Re-syncing the index with gitignore to be safe
echo [INFO] Refreshing Git Index...
git rm -r --cached . >nul 2>&1
git add .

echo.
echo ============================================
echo   FILES TO BE COMMITTED (Check carefully!)
echo ============================================
git status -s
echo ============================================
echo.

set /p commitmsg=Enter Commit Message (or press Enter for default): 

if "!commitmsg!"=="" (
    set commitmsg=Auto Commit - %date% %time%
)

echo.
echo [INFO] Creating commit...
git commit -m "!commitmsg!"

:: Check if remote exists before removing to avoid errors
git remote remove origin 2>nul
echo [INFO] Connecting to GitHub...
git remote add origin https://github.com/vsrepalle/youtube_video_upload_Mar14.git

echo [INFO] Setting main branch and pushing...
git branch -M main
git push -u origin main --force

echo.
echo ============================================
echo             PUSH COMPLETE
echo ============================================
pause