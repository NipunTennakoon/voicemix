"""
VoiceMix Configuration
"""

import os
from pathlib import Path

# Application settings
APP_NAME = "VoiceMix"
APP_VERSION = "1.0.0"
APP_AUTHOR = "VoiceMix Team"

# Directories
BASE_DIR = Path(__file__).parent.parent
TEMP_DIR = BASE_DIR / "temp_audio"
OUTPUT_DIR = BASE_DIR / "output"
MODELS_DIR = BASE_DIR / "models"

# Audio settings
SUPPORTED_FORMATS = ['.mp3']
DEFAULT_SAMPLE_RATE = 16000
MIN_SEGMENT_DURATION = 0.5  # seconds

# Processing settings
MAX_FILE_SIZE_MB = 500
ENABLE_CUDA = True

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "voicemix.log"

# UI settings
WINDOW_MIN_WIDTH = 700
WINDOW_MIN_HEIGHT = 600

# Create directories if they don't exist
TEMP_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
