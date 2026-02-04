# VoiceMix - MP3 Voice Processor

A desktop application for Windows 11 that processes MP3 files containing multiple voice dialogs, identifies different voices, selects the smoothest voice, and converts all other voices to match it, creating a unified voice tone in the output file.

## 📑 Table of Contents
- [Quick Start - Access the Interface](#-quick-start---access-the-interface)
- [Features](#features)
- [Installation](#installation)
- [Accessing the Interface](#️-accessing-the-interface)
- [Usage](#usage)
- [Documentation](#documentation)

## 🚀 Quick Start - Access the Interface

**Already have it installed?** Launch the application in one command:

```bash
# Windows
run_app.bat

# macOS/Linux
./run_app.sh
```

**First time user?** Set up and run:

```bash
# Windows
quick_start.bat

# macOS/Linux  
./quick_start.sh
```

**Need help?** See the complete guide: [How to Access the Interface](docs/HOW_TO_RUN.md)

---

## Features

- 🎤 **Speaker Diarization**: Automatically identify different speakers in audio files
- ✨ **Voice Quality Evaluation**: Select the smoothest and most ideal voice
- 🔄 **Voice Conversion**: Convert all voices to match the selected voice
- 🖥️ **User-Friendly GUI**: Intuitive drag-and-drop interface built with PyQt6
- 📊 **Real-Time Progress**: Visual feedback during processing
- 💾 **Easy Export**: Save processed files with a single click
- ⚡ **GPU Acceleration**: Supports CUDA for faster processing

## Screenshots

The application features a modern, clean interface with:
- Drag-and-drop zone for MP3 files
- Real-time progress bar
- One-click processing and download

## Requirements

### System Requirements
- **OS**: Windows 11 (also compatible with Windows 10, macOS, Linux)
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 2GB free space
- **Optional**: NVIDIA GPU with CUDA support for faster processing

### Software Requirements
- Python 3.8 or higher
- FFmpeg (for audio processing)

## Installation

### Option 1: Run from Source (Recommended for Development)

1. **Clone the repository**
   ```bash
   git clone https://github.com/NipunTennakoon/voicemix.git
   cd voicemix
   ```

2. **Install FFmpeg** (if not already installed)
   
   **Windows:**
   - Download FFmpeg from https://ffmpeg.org/download.html
   - Add FFmpeg to your system PATH
   
   **macOS:**
   ```bash
   brew install ffmpeg
   ```
   
   **Linux:**
   ```bash
   sudo apt-get install ffmpeg
   ```

3. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application** 🎉
   ```bash
   cd src
   python voicemix_app.py
   ```
   
   **Or use the convenient launcher:**
   ```bash
   # From the project root directory
   ./run_app.sh  # macOS/Linux
   # or
   run_app.bat  # Windows
   ```
   
   The application window will open with the VoiceMix interface!

### Option 2: Windows Executable (Coming Soon)

A standalone `.exe` file will be available for Windows users who don't want to install Python. Download from the [Releases](https://github.com/NipunTennakoon/voicemix/releases) page.

## 🖥️ Accessing the Interface

After installation, you have multiple ways to access the VoiceMix interface:

### Quick Launch (Recommended)
```bash
# Navigate to project directory
cd voicemix

# Run the launcher script
./run_app.sh     # macOS/Linux
run_app.bat      # Windows
```

### Manual Launch
```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Then run the application
cd src
python voicemix_app.py
```

### Troubleshooting Access Issues

If the interface doesn't appear:
1. **Verify installation:** `python verify_installation.py`
2. **Check dependencies:** Make sure all requirements are installed
3. **See detailed guide:** [How to Access the Interface](docs/HOW_TO_RUN.md)
4. **Check logs:** Look at `voicemix.log` for error messages

**Note:** VoiceMix is a desktop GUI application. You need a graphical environment (not just terminal) to access it.

## Usage

Once you've accessed the interface (see [How to Access](#-accessing-the-interface) above), follow these steps:

1. **Launch the application**
   - Run `./run_app.sh` (or `run_app.bat` on Windows)
   - Or run `python src/voicemix_app.py` from the project directory
   - The VoiceMix window will appear

2. **Select an MP3 file**
   - Drag and drop an MP3 file into the application window, or
   - Click "Browse Files" to select a file

3. **Start processing**
   - Click "Start Processing" button
   - The application will:
     - Analyze the audio to identify different speakers
     - Evaluate voice quality for each speaker
     - Select the best voice
     - Convert other voices to match the selected voice

4. **Save the result**
   - Once processing is complete, click "Save Processed File"
   - Choose where to save the unified MP3 file

**For detailed usage instructions with screenshots, see the [User Guide](docs/USER_GUIDE.md)**

## How It Works

### 1. Speaker Diarization
The application uses voice activity detection and audio feature analysis to identify segments where different speakers are talking.

### 2. Voice Quality Evaluation
Each speaker's voice is evaluated based on multiple acoustic features:
- Signal energy (clarity)
- Zero-crossing rate (smoothness)
- Spectral characteristics (tonal quality)

### 3. Voice Conversion
The application uses pitch shifting and spectral envelope matching to convert voices. This implementation provides a simplified voice conversion approach suitable for basic voice unification.

**Note**: For production-grade voice conversion, consider integrating:
- **pyannote-audio**: For advanced speaker diarization
- **Real-Time Voice Cloning (RTVC)**: For neural voice conversion
- **NVIDIA NeMo**: For enterprise-grade speech processing

## Building an Executable

To create a Windows executable:

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Create the executable**
   ```bash
   cd src
   pyinstaller --onefile --windowed --name VoiceMix --add-data "config.py;." voicemix_app.py
   ```

3. **Find the executable**
   - The `.exe` file will be in the `dist` folder
   - Distribute this file to users who don't have Python installed

## Project Structure

```
voicemix/
├── src/
│   ├── voicemix_app.py      # Main GUI application
│   ├── audio_processor.py   # Audio processing logic
│   ├── config.py            # Configuration settings
│   └── __init__.py          # Package initialization
├── tests/                   # Unit tests (future)
├── docs/                    # Additional documentation
├── resources/               # Icons, images, etc.
├── output/                  # Processed audio files
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Technical Details

### Audio Processing Pipeline

1. **Load Audio**: MP3 files are loaded and converted to mono if needed
2. **Diarization**: Voice activity detection identifies speaker segments
3. **Quality Assessment**: Each speaker is scored based on acoustic features
4. **Voice Selection**: The highest-quality voice is selected as the target
5. **Conversion**: Other speakers' voices are converted using pitch shifting
6. **Export**: The unified audio is saved as an MP3 file

### Libraries Used

- **PyQt6**: Modern GUI framework
- **pydub**: High-level audio manipulation
- **librosa**: Audio analysis and feature extraction
- **soundfile**: Audio file I/O
- **numpy/scipy**: Numerical processing
- **torch/torchaudio**: Deep learning support (optional, for advanced features)

## Limitations

This is a simplified implementation suitable for demonstration and basic use cases. For production use, consider:

1. **Advanced Diarization**: Integrate pyannote-audio for more accurate speaker detection
2. **Neural Voice Conversion**: Use RTVC or NeMo for higher-quality voice conversion
3. **Multi-threading**: Optimize for processing very long audio files
4. **Format Support**: Add support for more audio formats (WAV, M4A, etc.)

## Troubleshooting

### Common Issues

**Issue**: "FFmpeg not found"
- **Solution**: Install FFmpeg and ensure it's in your system PATH

**Issue**: Application is slow
- **Solution**: 
  - Enable CUDA if you have an NVIDIA GPU
  - Process shorter audio files
  - Close other applications to free up RAM

**Issue**: Poor voice conversion quality
- **Solution**: 
  - Ensure the input audio has good quality
  - Try files with clearer voice separation
  - Consider upgrading to neural-based voice conversion models

**Issue**: Can't access the interface / Application won't start
- **Solution**: See the comprehensive [How to Access the Interface](docs/HOW_TO_RUN.md) guide

## Documentation

Complete documentation is available in the `docs/` directory:

- **[How to Access the Interface](docs/HOW_TO_RUN.md)** ⭐ - Step-by-step guide to launching VoiceMix
- **[Setup Guide](docs/SETUP.md)** - Detailed installation for all platforms
- **[User Guide](docs/USER_GUIDE.md)** - Complete usage instructions with examples
- **[UI Guide](docs/UI_GUIDE.md)** - Interface navigation and features
- **[Advanced Configuration](docs/ADVANCED_CONFIG.md)** - Customization options

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests (when available)
5. Submit a pull request

## Future Enhancements

- [ ] Support for more audio formats (WAV, M4A, FLAC)
- [ ] Integration with pyannote-audio for better diarization
- [ ] Neural voice conversion using RTVC or NeMo
- [ ] Batch processing for multiple files
- [ ] Voice selection from UI (instead of automatic)
- [ ] Audio preview before and after processing
- [ ] Export settings (bitrate, format options)
- [ ] Multi-language support

## License

This project is open source and available under the MIT License.

## Acknowledgments

- PyQt6 for the excellent GUI framework
- librosa for audio analysis capabilities
- The open-source audio processing community

## Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This application uses simplified voice processing techniques suitable for basic voice unification. For professional-grade results, consider integrating advanced neural network models like those mentioned in the documentation.
