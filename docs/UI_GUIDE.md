# VoiceMix User Interface Guide

## Application Window

The VoiceMix application features a modern, intuitive interface divided into three main sections:

```
┌─────────────────────────────────────────────────────────────┐
│                        VoiceMix                             │
│     Convert multiple voices in MP3 files to a unified voice │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           1. Select MP3 File                        │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │   ┌─────────────────────────────────────────────┐  │   │
│  │   │  Drag & Drop MP3 file here                  │  │   │
│  │   │            or                                │  │   │
│  │   │  Click 'Browse' to select file              │  │   │
│  │   └─────────────────────────────────────────────┘  │   │
│  │                                                      │   │
│  │   [ 📁 Browse Files ]                               │   │
│  │                                                      │   │
│  │   Selected: example_audio.mp3                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           2. Process Audio                          │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │   [ 🎵 Start Processing ]                           │   │
│  │                                                      │   │
│  │   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░ 65%                │   │
│  │                                                      │   │
│  │   Converting voices to match target...              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           3. Download Result                        │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │   [ 💾 Save Processed File ]                        │   │
│  │                                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Interface Elements

### Section 1: File Selection
- **Drag-and-Drop Zone**: 
  - Large, highlighted area for dropping MP3 files
  - Changes color on hover and during drag
  - Visual feedback when file is accepted
  
- **Browse Button**: 
  - Blue button with file icon
  - Opens system file dialog
  - Filters to show only MP3 files
  
- **File Label**: 
  - Shows selected filename
  - Turns green when file is successfully loaded

### Section 2: Audio Processing
- **Start Processing Button**: 
  - Large green button
  - Only enabled when file is selected
  - Disabled during processing
  
- **Progress Bar**: 
  - Shows 0-100% progress
  - Updates in real-time
  - Color: Green for success, Red for errors
  
- **Status Label**: 
  - Shows current operation
  - Examples:
    - "Loading audio file..."
    - "Performing speaker diarization..."
    - "Converting segment 3/7..."
    - "Processing complete!"

### Section 3: Result Download
- **Save Button**: 
  - Orange button with save icon
  - Only enabled after successful processing
  - Opens file save dialog

## Color Scheme

- **Primary**: Blue (#2196F3) - Action buttons, highlights
- **Success**: Green (#4CAF50) - Process button, progress
- **Warning**: Orange (#FF9800) - Download button
- **Error**: Red (#f44336) - Error states
- **Background**: White (#FFFFFF)
- **Text**: Dark gray (#333333)
- **Borders**: Light gray (#ddd)

## Interactive States

### Drag-and-Drop States
1. **Idle**: Gray dashed border
2. **Hover**: Blue border, light blue background
3. **Active Drag**: Green border when MP3 detected
4. **Error**: Red flash for invalid files

### Button States
1. **Enabled**: Full color, interactive
2. **Hover**: Slightly darker color
3. **Pressed**: Much darker color
4. **Disabled**: Gray, non-interactive

### Progress States
1. **Ready**: 0%, gray
2. **Processing**: 1-99%, animated green
3. **Complete**: 100%, solid green
4. **Error**: Red with error message

## Dialog Boxes

### Success Dialog
```
┌─────────────────────────────────────────┐
│            Success                   ✓  │
├─────────────────────────────────────────┤
│                                          │
│  Audio processing completed              │
│  successfully!                           │
│                                          │
│  Click 'Save Processed File' to          │
│  download the result.                    │
│                                          │
│              [ OK ]                      │
└─────────────────────────────────────────┘
```

### Error Dialog
```
┌─────────────────────────────────────────┐
│         Processing Failed            ✗  │
├─────────────────────────────────────────┤
│                                          │
│  An error occurred during processing:    │
│                                          │
│  File format not supported              │
│                                          │
│              [ OK ]                      │
└─────────────────────────────────────────┘
```

### File Selection Dialog
```
┌─────────────────────────────────────────┐
│         Select MP3 File                  │
├─────────────────────────────────────────┤
│                                          │
│  Look in: ▼ Documents                    │
│                                          │
│  📁 Music                                │
│  📁 Downloads                            │
│  🎵 podcast_episode_1.mp3               │
│  🎵 interview_recording.mp3             │
│  🎵 voice_notes.mp3                     │
│                                          │
│  File name: __________________.mp3       │
│                                          │
│  Files of type: ▼ MP3 Files (*.mp3)     │
│                                          │
│         [ Open ]    [ Cancel ]           │
└─────────────────────────────────────────┘
```

## Processing Flow Visualization

```
User Action                System Response              Progress
───────────                ────────────────             ────────

[Drop file]    ───────>    Validate file                  0%
                           Check format
                           Check size
                           
                           ✓ File loaded               
                           Enable "Start" button

[Click Start]  ───────>    Initialize processor           5%
                           Load audio data               15%
                           
                           Perform diarization           30%
                           - Detect voice segments
                           - Identify speakers
                           
                           Evaluate voices               45%
                           - Score each speaker
                           - Select best voice
                           
                           Convert voices              45-90%
                           - Process segment 1
                           - Process segment 2
                           - ...
                           - Process segment N
                           
                           Save output file              95%
                           Clean up temp files          100%
                           
                           ✓ Processing complete
                           Enable "Save" button

[Click Save]   ───────>    Open save dialog
                           Copy to user location
                           
                           ✓ File saved
                           Show success message
```

## Keyboard Navigation

While the application primarily uses mouse/touch input, standard keyboard navigation works:

- **Tab**: Navigate between buttons
- **Enter**: Activate focused button
- **Escape**: Close dialogs
- **Ctrl+O**: Open file browser (when implemented)
- **Ctrl+S**: Save file (when available)

## Accessibility Features

- High contrast colors for visibility
- Clear visual feedback for all actions
- Descriptive status messages
- Error messages in plain language
- Keyboard navigation support
- Scalable UI elements

## Responsive Design

The window maintains a minimum size (700x600) but can be resized:
- Elements scale proportionally
- Text remains readable
- Buttons maintain usability
- Progress bar adjusts width

## Tips for Users

1. **Drag multiple files**: Only the last one is accepted (single-file mode)
2. **Progress stuck**: Wait for status message updates
3. **Large files**: May take several minutes to process
4. **Error messages**: Read carefully for troubleshooting hints
5. **Processing time**: Depends on file length and system speed

---

This interface design prioritizes:
- **Simplicity**: Clear, linear workflow
- **Feedback**: Always know what's happening
- **Efficiency**: Minimal clicks required
- **Error handling**: Graceful failure with helpful messages
- **Professional look**: Modern, clean appearance
