@echo off
setlocal EnableDelayedExpansion

title Build TrendWaveShorts EXE - PyInstaller

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║          Building standalone EXE for TrendWave             ║
echo ║         (Main entry: complete_video_workflow.py)           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

:: ────────────────────────────────────────────────
:: 1. Check / Install PyInstaller
:: ────────────────────────────────────────────────
echo [1] Checking PyInstaller...
python -m pip show pyinstaller >nul 2>&1

if %errorlevel% neq 0 (
echo PyInstaller not found → installing now...
python -m pip install --upgrade pip
python -m pip install pyinstaller

```
if %errorlevel% neq 0 (
    echo ERROR: Failed to install PyInstaller
    echo Try running this BAT file as Administrator
    pause
    exit /b 1
)
echo PyInstaller installed successfully.
```

) else (
echo PyInstaller is already installed.
)

:: ────────────────────────────────────────────────
:: 2. Clean previous builds
:: ────────────────────────────────────────────────
echo.
echo [2] Cleaning old build folders...

if exist build rd /s /q build
if exist dist rd /s /q dist
del /q *.spec 2>nul

echo Old builds cleaned.

:: ────────────────────────────────────────────────
:: 3. Build the executable
:: ────────────────────────────────────────────────
echo.
echo [3] Starting PyInstaller build...
echo    This may take 3–15 minutes (first build takes longest)
echo    Please wait...
echo.

pyinstaller ^
--onefile ^
--console ^
--name "TrendWaveShorts" ^
--add-data "data.json;." ^
--add-data "images\fetched;images\fetched" ^
--add-data "upload_to_youtube.py;." ^
--hidden-import flask ^
--hidden-import moviepy.editor ^
--hidden-import PIL ^
--hidden-import pyttsx3 ^
--exclude-module torch ^
--exclude-module tensorflow ^
--exclude-module transformers ^
--exclude-module scipy ^
--exclude-module numba ^
--exclude-module llvmlite ^
complete_video_workflow.py

if %errorlevel% neq 0 (
echo.
echo ╔════════════════════════════════════════════╗
echo ║               BUILD FAILED                 ║
echo ╚════════════════════════════════════════════╝
echo.
echo Possible reasons:
echo • Missing files/folders (data.json, images\fetched)
echo • PyInstaller dependency conflict
echo • Python environment issue
echo.
pause
exit /b 1
)

:: ────────────────────────────────────────────────
:: 4. Final message
:: ────────────────────────────────────────────────
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                  BUILD SUCCESSFUL                          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Your executable is here:
echo   %CD%\dist\TrendWaveShorts.exe
echo.
echo Double-click it to launch the full application.
echo.
echo Note:
echo - First run may take longer while dependencies extract.
echo - The console window will stay open for logs and input().
echo.

pause
