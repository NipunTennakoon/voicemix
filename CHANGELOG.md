# Changelog

All notable changes to VoiceMix will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-04

### Added
- Initial release of VoiceMix desktop application
- MP3 file processing with drag-and-drop interface
- Speaker diarization using energy-based voice activity detection
- Voice quality evaluation based on multiple acoustic features
- Voice conversion using pitch shifting and spectral matching
- PyQt6-based modern GUI with progress tracking
- Real-time progress feedback during processing
- Error handling and user-friendly dialogs
- Comprehensive documentation:
  - README with installation and usage instructions
  - Setup guide for Windows, macOS, and Linux
  - User guide with tips and best practices
  - Advanced configuration guide
  - Contributing guidelines
- Build scripts for creating Windows executables
- Quick start scripts for easy setup
- Installation verification script
- Unit tests for core audio processing functionality
- Support for GPU acceleration (CUDA)
- Configurable audio processing parameters
- Logging system for debugging

### Features
- **Multi-speaker Detection**: Automatically identifies different voices in audio
- **Intelligent Voice Selection**: Evaluates and selects the best quality voice
- **Voice Unification**: Converts all voices to match the selected target voice
- **User-Friendly Interface**: Intuitive drag-and-drop UI with visual feedback
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Extensible**: Modular design for easy enhancements

### Technical Details
- Python 3.8+ support
- PyQt6 for modern GUI
- librosa for audio analysis
- pydub for audio file handling
- NumPy/SciPy for numerical processing
- PyInstaller support for executable creation

## [Unreleased]

### Planned Features
- [ ] Support for additional audio formats (WAV, M4A, FLAC)
- [ ] Integration with pyannote.audio for advanced diarization
- [ ] Neural voice conversion using RTVC or NVIDIA NeMo
- [ ] Batch processing for multiple files
- [ ] Manual voice selection from UI
- [ ] Audio preview (before and after)
- [ ] Export settings (bitrate, format options)
- [ ] Multi-language UI support
- [ ] Improved voice conversion quality
- [ ] Real-time audio processing
- [ ] Cloud processing option
- [ ] Mobile app version

### Known Issues
- Voice conversion uses simplified algorithms (not neural networks)
- Limited to MP3 format currently
- Performance may be slow on systems without GPU
- Large files (>500MB) may cause memory issues

## Version History

- **1.0.0** (2026-02-04): Initial release

---

For more information, see the [GitHub repository](https://github.com/NipunTennakoon/voicemix).
