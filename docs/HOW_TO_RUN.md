# How to Access the VoiceMix Interface

This guide provides simple, step-by-step instructions for accessing and launching the VoiceMix application.

> **📌 Important Note:** VoiceMix is a **desktop application**, not a web application. There is no URL or web link to access it. You must download and run it locally on your computer.

## 🔗 Don't Have VoiceMix Yet?

If you don't have VoiceMix installed:

1. **Get the code**: https://github.com/NipunTennakoon/voicemix
   ```bash
   git clone https://github.com/NipunTennakoon/voicemix.git
   cd voicemix
   ```

2. **Or download Windows executable** (Coming Soon):
   - https://github.com/NipunTennakoon/voicemix/releases

After downloading, follow the installation instructions below.

---

## Quick Access Methods

### Method 1: One-Command Launch (Easiest) ⭐

If you just want to run the application quickly:

**Windows:**
```cmd
run_app.bat
```

**macOS/Linux:**
```bash
./run_app.sh
```

These scripts will automatically:
- Check for a virtual environment (create one if needed)
- Install dependencies if needed
- Launch the application

### Method 2: Manual Launch

If you prefer to do it manually:

1. **Navigate to the project directory:**
   ```bash
   cd voicemix
   ```

2. **Activate the virtual environment:**
   
   **Windows:**
   ```cmd
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

3. **Run the application:**
   ```bash
   cd src
   python voicemix_app.py
   ```

### Method 3: First-Time Setup

If this is your first time running VoiceMix:

**Windows:**
```cmd
quick_start.bat
```

**macOS/Linux:**
```bash
./quick_start.sh
```

This will:
1. Create a virtual environment
2. Install all dependencies
3. Provide instructions for running the app

Then use Method 1 or Method 2 to launch.

## What You'll See

When you successfully launch the application, you'll see:

```
┌─────────────────────────────────────────────────────────────┐
│                        VoiceMix                             │
│     Convert multiple voices in MP3 files to a unified voice │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           1. Select MP3 File                        │   │
│  │                                                      │   │
│  │   [Drag & Drop Zone]                                │   │
│  │   [ Browse Files ]                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           2. Process Audio                          │   │
│  │   [ Start Processing ]                              │   │
│  │   [Progress Bar: 0%]                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           3. Download Result                        │   │
│  │   [ Save Processed File ]                           │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Troubleshooting Access Issues

### Issue: "Command not found" or "File not found"

**Solution:**
Make sure you're in the correct directory:
```bash
cd /path/to/voicemix
```

### Issue: "Permission denied" (macOS/Linux)

**Solution:**
Make the scripts executable:
```bash
chmod +x run_app.sh quick_start.sh
```

### Issue: "Python not found"

**Solution:**
1. Check if Python is installed:
   ```bash
   python --version
   # or
   python3 --version
   ```

2. If not installed, download from [python.org](https://www.python.org/downloads/)

3. Make sure Python is in your system PATH

### Issue: "No module named 'PyQt6'" or other import errors

**Solution:**
Dependencies aren't installed. Run:
```bash
pip install -r requirements.txt
```

Or use the quick start script:
```bash
./quick_start.sh  # or quick_start.bat on Windows
```

### Issue: Application window doesn't appear

**Possible causes and solutions:**

1. **Display/Graphics issue:**
   - On Linux, you may need additional packages:
     ```bash
     sudo apt-get install libxcb-xinerama0 libxcb-cursor0
     ```

2. **Multiple displays:**
   - Check if the window opened on a different monitor
   - Try Alt+Tab (Windows/Linux) or Cmd+Tab (macOS)

3. **Firewall/Antivirus:**
   - Some security software may block Python GUI applications
   - Temporarily disable to test, then add exception

### Issue: "FFmpeg not found"

**Solution:**
Install FFmpeg:

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Add to system PATH

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

## Verifying Installation

Before trying to access the interface, verify everything is set up correctly:

```bash
python verify_installation.py
```

This will check:
- Python version
- Project structure
- Required directories
- Dependencies
- Module imports

## Alternative: Direct Python Command

If scripts aren't working, try directly:

```bash
python src/voicemix_app.py
```

Or with full path:

```bash
python /home/runner/work/voicemix/voicemix/src/voicemix_app.py
```

## Getting Help

If you still can't access the interface:

1. **Check the logs:**
   - Look for `voicemix.log` in the project directory
   - It may contain error messages

2. **Run verification:**
   ```bash
   python verify_installation.py
   ```

3. **Check system compatibility:**
   - Ensure your OS is supported (Windows 10+, macOS 10.14+, Ubuntu 18.04+)
   - Python 3.8 or higher required
   - 8GB RAM minimum

4. **Open an issue:**
   - Visit: https://github.com/NipunTennakoon/voicemix/issues
   - Include:
     - Your operating system and version
     - Python version
     - Error messages from logs
     - Output from `verify_installation.py`

## Next Steps

Once you've accessed the interface:
1. Read the [User Guide](USER_GUIDE.md) for detailed usage instructions
2. Check the [UI Guide](UI_GUIDE.md) for interface navigation
3. Review [Setup Guide](SETUP.md) for advanced configuration

---

## Quick Reference Card

| Task | Command |
|------|---------|
| **Quick Launch** | `./run_app.sh` or `run_app.bat` |
| **First Setup** | `./quick_start.sh` or `quick_start.bat` |
| **Manual Launch** | `cd src && python voicemix_app.py` |
| **Check Installation** | `python verify_installation.py` |
| **Install Dependencies** | `pip install -r requirements.txt` |
| **Activate venv (Unix)** | `source venv/bin/activate` |
| **Activate venv (Windows)** | `venv\Scripts\activate` |
| **Get VoiceMix** | `git clone https://github.com/NipunTennakoon/voicemix.git` |

---

## ❓ Frequently Asked Questions

### Is there a URL/link to access VoiceMix?
**No.** VoiceMix is a **desktop application**, not a web application. There's no URL to visit or web link to click. You need to:
1. Download/clone from: https://github.com/NipunTennakoon/voicemix
2. Install it on your computer
3. Run it locally using the commands above

### Where can I download VoiceMix?
- **Repository**: https://github.com/NipunTennakoon/voicemix (clone with git)
- **Releases**: https://github.com/NipunTennakoon/voicemix/releases (Windows .exe coming soon)

### Do I need internet to use VoiceMix?
No. Once installed, VoiceMix works **completely offline**. All processing happens on your local computer.

---

**Remember:** The interface is a desktop GUI application. You need a graphical environment (desktop) to access it. It won't work on headless servers without X11 forwarding or similar.
