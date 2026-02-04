"""
Unit tests for VoiceMix audio processor
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from audio_processor import AudioProcessor


class TestAudioProcessor:
    """Test cases for AudioProcessor class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.processor = AudioProcessor(temp_dir="test_temp")
    
    def teardown_method(self):
        """Cleanup after tests"""
        self.processor.cleanup()
    
    def test_initialization(self):
        """Test processor initialization"""
        assert self.processor is not None
        assert self.processor.temp_dir.exists()
    
    def test_voice_quality_evaluation(self):
        """Test voice quality evaluation"""
        # Create a simple sine wave as test audio
        sample_rate = 16000
        duration = 1.0
        frequency = 440.0  # A4 note
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = np.sin(2 * np.pi * frequency * t).astype(np.float32)
        
        quality_score = self.processor.evaluate_voice_quality(audio, sample_rate)
        
        assert isinstance(quality_score, (float, np.floating))
        assert quality_score > 0
    
    def test_diarization(self):
        """Test speaker diarization"""
        # Create test audio with silent and active regions
        sample_rate = 16000
        duration = 5.0
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Create audio with periodic activity
        audio = np.zeros_like(t, dtype=np.float32)
        for i in range(0, len(t), sample_rate):  # 1 second intervals
            if (i // sample_rate) % 2 == 0:  # Every other second
                end_idx = min(i + sample_rate, len(t))
                audio[i:end_idx] = np.sin(2 * np.pi * 440 * t[i:end_idx])
        
        segments = self.processor.perform_diarization(audio, sample_rate)
        
        assert isinstance(segments, list)
        assert len(segments) > 0
        for seg in segments:
            assert 'speaker' in seg
            assert 'start' in seg
            assert 'end' in seg
            assert seg['end'] > seg['start']
    
    def test_voice_conversion(self):
        """Test voice conversion"""
        sample_rate = 16000
        duration = 1.0
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Source audio at 440 Hz
        source = np.sin(2 * np.pi * 440 * t).astype(np.float32)
        
        # Target audio at 550 Hz
        target = np.sin(2 * np.pi * 550 * t).astype(np.float32)
        
        converted = self.processor.convert_voice(source, target, sample_rate)
        
        assert isinstance(converted, np.ndarray)
        assert len(converted) > 0
        assert converted.dtype == np.float32 or converted.dtype == np.float64
    
    def test_select_best_voice(self):
        """Test best voice selection"""
        sample_rate = 16000
        duration = 5.0
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = np.sin(2 * np.pi * 440 * t).astype(np.float32)
        
        segments = [
            {'speaker': 'SPEAKER_00', 'start': 0.0, 'end': 1.5},
            {'speaker': 'SPEAKER_01', 'start': 1.5, 'end': 3.0},
            {'speaker': 'SPEAKER_00', 'start': 3.0, 'end': 4.5},
        ]
        
        best_speaker, best_segment = self.processor.select_best_voice(
            audio, sample_rate, segments
        )
        
        assert isinstance(best_speaker, str)
        assert best_speaker.startswith('SPEAKER_')
        assert isinstance(best_segment, dict)
        assert 'start' in best_segment
        assert 'end' in best_segment


def test_imports():
    """Test that all required modules can be imported"""
    try:
        import numpy
        import librosa
        import soundfile
        from pydub import AudioSegment
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import required module: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
