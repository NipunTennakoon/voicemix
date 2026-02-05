@echo off
REM Run VoiceMix application

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Running quick start...
    call quick_start.bat
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the application
cd src
python voicemix_app.py
