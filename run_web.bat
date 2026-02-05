@echo off
REM Run VoiceMix Web Application

echo ==========================================
echo Starting VoiceMix Web Application
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Running quick start...
    call quick_start.bat
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Navigate to src directory
cd src

REM Run the web application
echo Starting Flask server...
echo Access the application at: http://localhost:5000
echo.
python web_app.py
