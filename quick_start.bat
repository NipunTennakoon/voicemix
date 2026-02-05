@echo off
REM Quick start script for VoiceMix (Windows)

echo ==========================================
echo VoiceMix Quick Start
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do echo ✓ Python found: %%i
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install dependencies
echo.
echo Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt

echo.
echo ==========================================
echo Installation complete!
echo ==========================================
echo.
echo To run VoiceMix:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate.bat
echo   2. Run the application:
echo      cd src
echo      python voicemix_app.py
echo.
echo Or simply run: run_app.bat
echo.

pause
