# VoiceMix - MP3 Voice Processor

A **web application** that processes MP3 files containing multiple voice dialogs, identifies different voices, selects the smoothest voice, and converts all other voices to match it, creating a unified voice tone in the output file.

> **🌐 Web-Based:** VoiceMix is now a **web application**! Access it through your browser at `http://localhost:5000` after starting the server. Upload MP3 files and download the processed results directly from the dashboard.

## 📑 Table of Contents
- [Getting Started](#-getting-started)
- [Quick Start - Launch Web App](#-quick-start---launch-web-app)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)

## 🔗 Getting Started

**VoiceMix runs as a local web server** on your computer.

To get VoiceMix:

1. **Clone from GitHub** (Recommended):
   ```bash
   git clone https://github.com/NipunTennakoon/voicemix.git
   cd voicemix
   ```
   📍 Repository: https://github.com/NipunTennakoon/voicemix

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

After installation, see [Quick Start](#-quick-start---launch-web-app) to launch the web server.

## 🚀 Quick Start - Launch Web App

**Launch the web application:**

```bash
# Windows
run_web.bat

# macOS/Linux
./run_web.sh
```

**Then access the dashboard in your browser:**
- Open: `http://localhost:5000`
- Upload MP3 files
- Monitor processing progress
- Download unified audio

**First time user?** Set up dependencies first:

```bash
# Windows
quick_start.bat

# macOS/Linux  
./quick_start.sh
```

---

## Features

- 🎤 **Speaker Diarization**: Automatically identify different speakers in audio files
- ✨ **Voice Quality Evaluation**: Select the smoothest and most ideal voice
- 🔄 **Voice Conversion**: Convert all voices to match the selected voice
- 🌐 **Web Dashboard**: Intuitive web interface with drag-and-drop upload
- 📊 **Real-Time Progress**: Visual feedback during processing
- 💾 **Easy Download**: Download processed files with one click
- ⚡ **GPU Acceleration**: Supports CUDA for faster processing

## Screenshots

The web application features a modern dashboard with:
- Drag-and-drop zone for MP3 file uploads
- Real-time progress bar with status updates
- One-click download of processed files
- Responsive design for all devices

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

A standalone deployment option will be available in the future. For now, run the web server locally.

## 🌐 Accessing the Web Interface

After installation, launch the web server:

### Quick Launch (Recommended)
```bash
# Navigate to project directory
cd voicemix

# Run the web server
./run_web.sh     # macOS/Linux
run_web.bat      # Windows
```

### Access the Dashboard
1. Start the web server using the command above
2. Open your browser
3. Navigate to: `http://localhost:5000`
4. You'll see the VoiceMix dashboard

### Manual Launch
```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Then run the web application
cd src
python web_app.py
```

Then open `http://localhost:5000` in your browser.

### Troubleshooting Access Issues

If the interface doesn't appear:
1. **Check if server is running:** Look for "Running on http://0.0.0.0:5000" message
2. **Verify port is available:** Make sure port 5000 is not in use
3. **Check firewall:** Ensure firewall allows connections to localhost:5000
4. **Try different browser:** Chrome, Firefox, or Edge recommended
5. **Check logs:** Look at `voicemix_web.log` for error messages

## Usage

Once you've launched the web server and accessed the dashboard:

1. **Launch the web application**
   - Run `./run_web.sh` (or `run_web.bat` on Windows)
   - Open browser and go to `http://localhost:5000`
   - You'll see the VoiceMix dashboard

2. **Upload an MP3 file**
   - **Drag and drop** an MP3 file into the upload zone, or
   - Click **"Browse Files"** to select a file from your computer
   - File will be uploaded automatically

3. **Monitor processing**
   - Watch the progress bar showing processing status
   - Status messages will update in real-time:
     - "Loading audio file..."
     - "Performing speaker diarization..."
     - "Converting voices..."
     - "Processing complete!"

4. **Download the result**
   - Once processing is complete, click **"Download Processed File"**
   - The unified MP3 file will be downloaded to your computer
   - Click **"Process Another File"** to start over

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

## ❓ FAQ

### Is VoiceMix a website or web application?
**No.** VoiceMix is a **desktop application** that runs locally on your computer. There is no website or URL to visit. You need to:
1. Download or clone the application from GitHub
2. Install it on your computer
3. Run it locally

### Can I get a link to access the interface?
VoiceMix doesn't have a web link or URL because it's not a web application. To access the interface:
- **Repository link**: https://github.com/NipunTennakoon/voicemix (to download/clone)
- **Run locally**: After installation, use `./run_app.sh` or `run_app.bat` to launch the desktop GUI

See [Getting the Application](#-getting-the-application) for download options.

### Where can I download VoiceMix?
- **Source Code**: Clone from https://github.com/NipunTennakoon/voicemix
- **Windows Executable**: Coming soon at https://github.com/NipunTennakoon/voicemix/releases

### Do I need an internet connection to use VoiceMix?
No. Once installed, VoiceMix works **completely offline**. All processing happens locally on your computer.

### Can I use VoiceMix from a browser?
No. VoiceMix is a desktop GUI application built with PyQt6. It requires installation and runs as a desktop application, not in a web browser.

### What's the difference between a desktop app and a web app?
- **Desktop App** (VoiceMix): Installed on your computer, runs locally, no URL needed
- **Web App**: Accessed through a browser via a URL/link, runs on a server

VoiceMix is a desktop application for better performance, privacy, and offline functionality.

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
