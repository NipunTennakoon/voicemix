@echo off
REM Build script for VoiceMix Windows executable

echo ========================================
echo VoiceMix Build Script for Windows
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Install PyInstaller if not already installed
echo Installing PyInstaller...
pip install pyinstaller

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Build the executable
echo.
echo ========================================
echo Building executable...
echo ========================================
pyinstaller voicemix.spec

REM Check if build was successful
if exist "dist\VoiceMix.exe" (
    echo.
    echo ========================================
    echo Build completed successfully!
    echo ========================================
    echo.
    echo Executable location: dist\VoiceMix.exe
    echo.
    echo You can now distribute the VoiceMix.exe file.
    echo Make sure to include FFmpeg in the distribution if needed.
    echo.
) else (
    echo.
    echo ========================================
    echo Build failed!
    echo ========================================
    echo Please check the error messages above.
    echo.
)

pause
