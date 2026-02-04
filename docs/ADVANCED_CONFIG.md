# Advanced Configuration for VoiceMix

This document describes advanced configuration options for VoiceMix.

## Configuration File

The main configuration is located in `src/config.py`. You can modify these settings to customize the application behavior.

## Available Settings

### Application Settings

```python
APP_NAME = "VoiceMix"
APP_VERSION = "1.0.0"
```

### Directories

```python
BASE_DIR = Path(__file__).parent.parent
TEMP_DIR = BASE_DIR / "temp_audio"      # Temporary processing files
OUTPUT_DIR = BASE_DIR / "output"         # Processed audio output
MODELS_DIR = BASE_DIR / "models"         # ML models (if used)
```

### Audio Settings

```python
SUPPORTED_FORMATS = ['.mp3']             # Add more formats: ['.mp3', '.wav', '.m4a']
DEFAULT_SAMPLE_RATE = 16000              # Sample rate for processing
MIN_SEGMENT_DURATION = 0.5               # Minimum voice segment duration in seconds
```

### Processing Settings

```python
MAX_FILE_SIZE_MB = 500                   # Maximum input file size
ENABLE_CUDA = True                       # Use GPU if available
```

### Logging

```python
LOG_LEVEL = "INFO"                       # Options: DEBUG, INFO, WARNING, ERROR
LOG_FILE = "voicemix.log"                # Log file location
```

### UI Settings

```python
WINDOW_MIN_WIDTH = 700                   # Minimum window width
WINDOW_MIN_HEIGHT = 600                  # Minimum window height
```

## Advanced Audio Processing

### Voice Quality Evaluation Weights

To modify how voice quality is evaluated, edit the `evaluate_voice_quality` method in `src/audio_processor.py`:

```python
quality_score = (
    energy * 10 +                        # Energy contribution (increase for louder preference)
    (1 - zcr) * 5 +                      # ZCR contribution (increase for smoother preference)
    (1 / (1 + spectral_centroid / 1000)) * 3 +  # Spectral centroid
    (1 / (1 + spectral_rolloff / 1000)) * 2     # Spectral rolloff
)
```

### Diarization Parameters

In `perform_diarization` method:

```python
frame_length = int(0.025 * sample_rate)  # Frame length in seconds
hop_length = int(0.010 * sample_rate)    # Hop length in seconds
threshold = np.mean(energy) * 0.5        # Voice activity threshold (0.0-1.0)
```

Adjust these values for:
- **Longer frame_length**: More stable detection, less responsive
- **Higher threshold**: Detect only louder voices
- **Lower threshold**: Detect quieter voices

### Voice Conversion Range

In `convert_voice` method:

```python
pitch_shift = np.clip(pitch_shift, -5, 5)  # Limit pitch shift range (semitones)
```

Adjust the range:
- **Smaller range (-2, 2)**: More conservative, natural-sounding conversions
- **Larger range (-12, 12)**: More dramatic transformations

## Integration with Advanced Models

### Using pyannote.audio for Diarization

To use pyannote.audio instead of the simplified implementation:

1. Install pyannote.audio:
   ```bash
   pip install pyannote.audio
   ```

2. Modify `perform_diarization` in `audio_processor.py`:

```python
from pyannote.audio import Pipeline

def perform_diarization(self, audio_file: str) -> List[Dict]:
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")
    diarization = pipeline(audio_file)
    
    segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        segments.append({
            'speaker': speaker,
            'start': turn.start,
            'end': turn.end
        })
    
    return segments
```

### Using Real-Time Voice Cloning

To integrate RTVC for neural voice conversion:

1. Install RTVC:
   ```bash
   git clone https://github.com/CorentinJ/Real-Time-Voice-Cloning.git
   # Follow RTVC installation instructions
   ```

2. Add to `audio_processor.py`:

```python
from encoder import inference as encoder
from vocoder import inference as vocoder
from synthesizer.inference import Synthesizer

def neural_voice_conversion(self, source_audio, target_audio, sample_rate):
    # Load models
    encoder.load_model(Path("models/encoder.pt"))
    vocoder.load_model(Path("models/vocoder.pt"))
    synthesizer = Synthesizer(Path("models/synthesizer.pt"))
    
    # Generate embedding from target voice
    target_embed = encoder.embed_utterance(target_audio)
    
    # Convert source to target
    # Implementation depends on RTVC API
    converted = synthesizer.synthesize_spectrograms(source_audio, target_embed)
    
    return converted
```

## Performance Optimization

### GPU Acceleration

Ensure CUDA is properly configured:

```python
# In audio_processor.py __init__
self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

### Multi-threading

For processing multiple files:

```python
from concurrent.futures import ThreadPoolExecutor

def batch_process(files):
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(process_audio_file, files)
    return list(results)
```

## Environment Variables

You can use environment variables for configuration:

Create a `.env` file:

```bash
VOICEMIX_MAX_FILE_SIZE=1000
VOICEMIX_CUDA_ENABLED=true
VOICEMIX_LOG_LEVEL=DEBUG
```

Then in `config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

MAX_FILE_SIZE_MB = int(os.getenv('VOICEMIX_MAX_FILE_SIZE', '500'))
ENABLE_CUDA = os.getenv('VOICEMIX_CUDA_ENABLED', 'true').lower() == 'true'
LOG_LEVEL = os.getenv('VOICEMIX_LOG_LEVEL', 'INFO')
```

## Troubleshooting Configuration

### Memory Issues

Reduce memory usage:

```python
# Process audio in chunks
CHUNK_SIZE = 30  # seconds
MAX_CONCURRENT_CHUNKS = 2
```

### Quality vs Speed

Trade-off configurations:

**Fast Processing (Lower Quality)**:
```python
DEFAULT_SAMPLE_RATE = 16000
frame_length = int(0.050 * sample_rate)  # Larger frames
```

**High Quality (Slower)**:
```python
DEFAULT_SAMPLE_RATE = 44100
frame_length = int(0.010 * sample_rate)  # Smaller frames
```

## Custom UI Themes

Modify styles in `voicemix_app.py`:

```python
# Dark theme example
self.setStyleSheet("""
    QMainWindow {
        background-color: #2b2b2b;
    }
    QLabel {
        color: #ffffff;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px;
    }
""")
```

## Plugin System (Future)

For extending functionality:

```python
# plugins/my_processor.py
class MyCustomProcessor:
    def process(self, audio_data, sample_rate):
        # Custom processing
        return processed_audio

# Register plugin
PLUGINS = [
    MyCustomProcessor(),
    # Add more plugins
]
```

## Getting Help

For advanced configuration questions:
- Open an issue on GitHub
- Check the source code documentation
- Consult the community forums

---

Remember to test thoroughly after making configuration changes!
