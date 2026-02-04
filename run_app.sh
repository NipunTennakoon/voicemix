#!/bin/bash
# Run VoiceMix application

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running quick start..."
    ./quick_start.sh
    echo ""
fi

# Activate virtual environment
source venv/bin/activate

# Run the application
cd src
python voicemix_app.py
