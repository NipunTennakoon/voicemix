# Setup and Installation Guide

This guide provides detailed instructions for setting up VoiceMix on different platforms.

## Table of Contents
1. [Windows Setup](#windows-setup)
2. [macOS Setup](#macos-setup)
3. [Linux Setup](#linux-setup)
4. [Troubleshooting](#troubleshooting)

---

## Windows Setup

### Prerequisites

1. **Python 3.8+**
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **FFmpeg**
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html#build-windows)
   - Extract to a directory (e.g., `C:\ffmpeg`)
   - Add to PATH:
     1. Search "Environment Variables" in Windows
     2. Click "Environment Variables"
     3. Under "System variables", find "Path" and click "Edit"
     4. Click "New" and add the FFmpeg bin directory (e.g., `C:\ffmpeg\bin`)
     5. Click "OK" to save

3. **Git** (optional)
   - Download from [git-scm.com](https://git-scm.com/download/win)

### Installation Steps

1. **Clone or Download the Repository**
   ```cmd
   git clone https://github.com/NipunTennakoon/voicemix.git
   cd voicemix
   ```

2. **Create Virtual Environment**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```cmd
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```cmd
   cd src
   python voicemix_app.py
   ```

### Building Windows Executable

```cmd
pip install pyinstaller
pyinstaller voicemix.spec
```

The executable will be in the `dist` folder.

---

## macOS Setup

### Prerequisites

1. **Python 3.8+**
   - Install via Homebrew: `brew install python@3.11`
   - Or download from [python.org](https://www.python.org/downloads/)

2. **FFmpeg**
   ```bash
   brew install ffmpeg
   ```

3. **Git**
   ```bash
   brew install git
   ```

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/NipunTennakoon/voicemix.git
   cd voicemix
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   cd src
   python voicemix_app.py
   ```

---

## Linux Setup

### Prerequisites (Ubuntu/Debian)

1. **Python 3.8+**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

2. **FFmpeg**
   ```bash
   sudo apt install ffmpeg
   ```

3. **Git**
   ```bash
   sudo apt install git
   ```

4. **Additional Libraries** (for PyQt6)
   ```bash
   sudo apt install libxcb-xinerama0 libxcb-cursor0
   ```

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/NipunTennakoon/voicemix.git
   cd voicemix
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   cd src
   python voicemix_app.py
   ```

---

## Troubleshooting

### FFmpeg Not Found

**Problem**: Application can't find FFmpeg

**Solutions**:
- Windows: Ensure FFmpeg is in PATH (restart terminal after adding)
- macOS: Run `brew install ffmpeg`
- Linux: Run `sudo apt install ffmpeg`
- Verify installation: `ffmpeg -version`

### PyQt6 Installation Fails

**Problem**: Error installing PyQt6

**Solutions**:
- Update pip: `pip install --upgrade pip`
- On Linux, install system dependencies:
  ```bash
  sudo apt install python3-pyqt6 libxcb-xinerama0
  ```
- Try PyQt5 instead: Edit requirements.txt to use `PyQt5>=5.15.0`

### CUDA/GPU Issues

**Problem**: CUDA not detected or errors

**Solutions**:
- Ensure NVIDIA drivers are installed
- Install CUDA toolkit from [NVIDIA website](https://developer.nvidia.com/cuda-downloads)
- The application works fine on CPU, just slower

### Memory Errors

**Problem**: Out of memory during processing

**Solutions**:
- Process shorter audio files
- Close other applications
- Increase system virtual memory/swap
- Use a machine with more RAM (16GB recommended)

### Permission Errors

**Problem**: Cannot write to output directory

**Solutions**:
- Windows: Run as administrator
- macOS/Linux: Check folder permissions
  ```bash
  chmod -R 755 /path/to/voicemix
  ```

### Application Won't Start

**Problem**: Application crashes on startup

**Solutions**:
1. Check Python version: `python --version` (need 3.8+)
2. Reinstall dependencies:
   ```bash
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt
   ```
3. Check logs in `voicemix.log`
4. Run with debug output:
   ```bash
   python voicemix_app.py --verbose
   ```

---

## Advanced Configuration

### Using CUDA for GPU Acceleration

1. Install CUDA toolkit
2. Install PyTorch with CUDA:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

### Customizing Settings

Edit `src/config.py` to modify:
- Maximum file size
- Audio processing parameters
- Temporary directory location
- Output directory

---

## Getting Help

If you encounter issues not covered here:

1. Check the [Issues page](https://github.com/NipunTennakoon/voicemix/issues)
2. Search for similar problems
3. Open a new issue with:
   - Your OS and version
   - Python version
   - Full error message
   - Steps to reproduce

---

## System Requirements Summary

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Windows 10, macOS 10.14, Ubuntu 18.04 | Windows 11, macOS 12+, Ubuntu 22.04 |
| Python | 3.8 | 3.10+ |
| RAM | 8 GB | 16 GB |
| Storage | 2 GB | 5 GB |
| GPU | Not required | NVIDIA with CUDA support |
