#!/bin/bash
# Run VoiceMix Web Application

echo "=========================================="
echo "Starting VoiceMix Web Application"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running quick start..."
    ./quick_start.sh
    echo ""
fi

# Activate virtual environment
source venv/bin/activate

# Navigate to src directory
cd src

# Run the web application
echo "Starting Flask server..."
echo "Access the application at: http://localhost:5000"
echo ""
python web_app.py
