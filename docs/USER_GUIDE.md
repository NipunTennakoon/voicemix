# VoiceMix User Guide

Complete guide for using the VoiceMix desktop application.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Interface Overview](#interface-overview)
3. [Processing Audio Files](#processing-audio-files)
4. [Understanding Results](#understanding-results)
5. [Tips and Best Practices](#tips-and-best-practices)
6. [FAQ](#faq)

---

## Getting Started

### Launching the Application

**From Source:**
```bash
cd voicemix/src
python voicemix_app.py
```

**From Executable (Windows):**
- Double-click `VoiceMix.exe`

### First Run

On first launch, the application will:
1. Create necessary directories (`output/`, `temp_audio/`)
2. Initialize the audio processor
3. Display the main interface

---

## Interface Overview

The VoiceMix interface is divided into three main sections:

### 1. Select MP3 File Section
- **Drag & Drop Zone**: Drop MP3 files here for quick upload
- **Browse Button**: Click to open file browser
- **File Label**: Shows the currently selected file

### 2. Process Audio Section
- **Start Processing Button**: Begins audio processing
- **Progress Bar**: Shows processing progress (0-100%)
- **Status Label**: Displays current operation

### 3. Download Result Section
- **Save Processed File Button**: Save the unified audio file
- Enabled after successful processing

---

## Processing Audio Files

### Step 1: Select an MP3 File

**Method A: Drag and Drop**
1. Locate your MP3 file in File Explorer
2. Drag the file over the application window
3. Drop it in the designated drop zone
4. The file name will appear below the zone

**Method B: Browse**
1. Click the "Browse Files" button
2. Navigate to your MP3 file
3. Select the file and click "Open"

**Supported Formats:**
- Currently: MP3 files only
- File size: Up to 500 MB (configurable)

### Step 2: Start Processing

1. Click the "Start Processing" button
2. The application will:
   - **Load the audio file** (5-15%)
   - **Analyze speakers** (15-30%): Identify different voices
   - **Select best voice** (30-45%): Evaluate voice quality
   - **Convert voices** (45-90%): Match all voices to the best one
   - **Save output** (90-100%): Create the final MP3

**Processing Time:**
- Depends on file length and system specs
- Typical: 1-2 minutes per minute of audio
- With GPU: 2-3x faster

### Step 3: Save the Result

1. Wait for "Processing completed successfully!" message
2. Click "Save Processed File"
3. Choose a location and filename
4. Click "Save"

The unified MP3 file is now ready to use!

---

## Understanding Results

### What Happens During Processing

1. **Speaker Diarization**
   - The application analyzes the audio waveform
   - Identifies segments where different people speak
   - Creates a timeline of speaker activity

2. **Voice Quality Evaluation**
   - Each speaker is scored on:
     - **Clarity**: Signal strength and noise level
     - **Smoothness**: Vocal steadiness
     - **Tonal Quality**: Frequency characteristics
   - The highest-scoring voice is selected

3. **Voice Conversion**
   - Other speakers' voices are modified to match the target
   - Pitch is adjusted to match
   - Spectral characteristics are aligned
   - Original timing and content preserved

### Expected Results

**Good Results:**
- Audio with 2-5 distinct speakers
- Clear voice recordings (minimal background noise)
- Similar speaking styles
- Good recording quality

**May Need Improvement:**
- Very noisy audio
- More than 5 speakers
- Very different voice types (child + adult)
- Poor recording quality

---

## Tips and Best Practices

### For Best Results

1. **Audio Quality**
   - Use high-quality MP3 files (128 kbps or higher)
   - Minimize background noise
   - Ensure clear voice separation

2. **File Preparation**
   - Remove long silent sections
   - Trim to relevant content
   - Keep files under 100 MB for faster processing

3. **Speaker Characteristics**
   - Works best with similar voice types
   - Better results with 2-4 speakers
   - Similar speaking volumes help

### Optimization Tips

1. **Performance**
   - Close other applications during processing
   - Use GPU if available (2-3x faster)
   - Process shorter files for testing

2. **Quality**
   - Start with high-quality source files
   - Avoid heavily compressed audio
   - Test with short samples first

---

## FAQ

### General Questions

**Q: What audio formats are supported?**
A: Currently, only MP3 files. WAV, M4A support planned for future versions.

**Q: How long does processing take?**
A: Approximately 1-2 minutes per minute of audio on a modern CPU. Faster with GPU.

**Q: Is my audio data stored or uploaded?**
A: No. All processing happens locally on your computer. Files are not uploaded anywhere.

**Q: Can I process multiple files at once?**
A: Not currently. Batch processing is planned for a future update.

### Technical Questions

**Q: Why is the result quality not perfect?**
A: This application uses simplified voice conversion. For professional results, consider using advanced neural network models like RTVC or NeMo.

**Q: Can I choose which voice to use as the target?**
A: Currently, the best voice is selected automatically. Manual selection is planned for future versions.

**Q: What if I have more than 5 speakers?**
A: The application can handle any number of speakers, but quality may decrease with more than 5 distinct voices.

**Q: Does this require an internet connection?**
A: No. VoiceMix works completely offline.

### Troubleshooting

**Q: Processing failed - what should I do?**
A: 
1. Check the error message
2. Verify file is a valid MP3
3. Try a smaller file
4. Check `voicemix.log` for details
5. Restart the application

**Q: The application is very slow**
A: 
1. Close other applications
2. Process shorter files
3. Check if GPU acceleration is available
4. Ensure sufficient RAM (8GB minimum)

**Q: Output quality is poor**
A:
1. Use higher-quality source files
2. Ensure clear voice separation in original
3. Try files with similar speaker characteristics
4. Consider using professional voice conversion tools

**Q: File won't load**
A:
1. Verify it's an MP3 file
2. Check file isn't corrupted (play in media player)
3. Ensure file size is under 500 MB
4. Try converting to MP3 using another tool first

---

## Keyboard Shortcuts

Currently, the application uses mouse/touch input only. Keyboard shortcuts may be added in future versions.

---

## Support

For additional help:
- Check the main [README.md](../README.md)
- Review [SETUP.md](SETUP.md) for installation issues
- Visit the [GitHub Issues](https://github.com/NipunTennakoon/voicemix/issues) page
- Open a new issue with your question

---

## Feedback

We welcome your feedback! Please share:
- Feature suggestions
- Bug reports
- Use cases
- Improvement ideas

Open an issue on GitHub or contribute via pull requests.
