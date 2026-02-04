#!/bin/bash
# Build script for VoiceMix (macOS/Linux)

echo "========================================"
echo "VoiceMix Build Script"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Install PyInstaller
echo "Installing PyInstaller..."
pip install pyinstaller

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Build the executable
echo ""
echo "========================================"
echo "Building executable..."
echo "========================================"
pyinstaller voicemix.spec

# Check if build was successful
if [ -f "dist/VoiceMix" ] || [ -f "dist/VoiceMix.app/Contents/MacOS/VoiceMix" ]; then
    echo ""
    echo "========================================"
    echo "Build completed successfully!"
    echo "========================================"
    echo ""
    echo "Executable location: dist/"
    echo ""
    echo "You can now distribute the VoiceMix executable."
    echo "Make sure to include FFmpeg in the distribution if needed."
    echo ""
else
    echo ""
    echo "========================================"
    echo "Build failed!"
    echo "========================================"
    echo "Please check the error messages above."
    echo ""
    exit 1
fi
