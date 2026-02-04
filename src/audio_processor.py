"""
VoiceMix - Audio Processing Module
Handles speaker diarization, voice quality evaluation, and voice conversion
"""

import os
import logging
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import numpy as np
import soundfile as sf
import librosa
from pydub import AudioSegment
from pydub.effects import normalize
import torch

logger = logging.getLogger(__name__)


class AudioProcessor:
    """Main class for audio processing operations"""
    
    def __init__(self, temp_dir: str = "temp_audio"):
        """
        Initialize AudioProcessor
        
        Args:
            temp_dir: Directory for temporary audio files
        """
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(exist_ok=True)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"AudioProcessor initialized with device: {self.device}")
        
    def load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Load audio file and convert to numpy array
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        logger.info(f"Loading audio from: {file_path}")
        
        # Use pydub to handle MP3 files
        audio = AudioSegment.from_mp3(file_path)
        
        # Convert to mono if stereo
        if audio.channels > 1:
            audio = audio.set_channels(1)
            
        # Get audio data and sample rate
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
        samples = samples / (2**15)  # Normalize to [-1, 1]
        sample_rate = audio.frame_rate
        
        logger.info(f"Audio loaded: duration={len(audio)/1000:.2f}s, sr={sample_rate}Hz")
        return samples, sample_rate
    
    def save_audio(self, audio_data: np.ndarray, sample_rate: int, 
                   output_path: str, format: str = "mp3") -> None:
        """
        Save audio data to file
        
        Args:
            audio_data: Audio samples
            sample_rate: Sample rate
            output_path: Output file path
            format: Output format (mp3, wav)
        """
        logger.info(f"Saving audio to: {output_path}")
        
        # Normalize audio data
        audio_data = np.clip(audio_data, -1.0, 1.0)
        audio_int16 = (audio_data * 32767).astype(np.int16)
        
        # Save as WAV first
        temp_wav = self.temp_dir / "temp_output.wav"
        sf.write(temp_wav, audio_int16, sample_rate)
        
        # Convert to MP3 if needed
        if format.lower() == "mp3":
            audio_segment = AudioSegment.from_wav(str(temp_wav))
            audio_segment = normalize(audio_segment)
            audio_segment.export(output_path, format="mp3", bitrate="192k")
            temp_wav.unlink()
        else:
            sf.write(output_path, audio_int16, sample_rate)
            
        logger.info(f"Audio saved successfully")
    
    def perform_diarization(self, audio_data: np.ndarray, 
                           sample_rate: int) -> List[Dict]:
        """
        Perform speaker diarization to identify different speakers
        
        This is a simplified implementation using energy-based voice activity detection
        and clustering. For production, use pyannote.audio or speechbrain.
        
        Args:
            audio_data: Audio samples
            sample_rate: Sample rate
            
        Returns:
            List of speaker segments with format:
            [{'speaker': 'SPEAKER_00', 'start': 0.0, 'end': 2.5}, ...]
        """
        logger.info("Performing speaker diarization (simplified)")
        
        # Calculate frame-level energy
        frame_length = int(0.025 * sample_rate)  # 25ms frames
        hop_length = int(0.010 * sample_rate)    # 10ms hop
        
        # Compute energy
        energy = librosa.feature.rms(y=audio_data, 
                                    frame_length=frame_length, 
                                    hop_length=hop_length)[0]
        
        # Voice activity detection (simple threshold-based)
        threshold = np.mean(energy) * 0.5
        voice_activity = energy > threshold
        
        # Find continuous segments
        segments = []
        in_segment = False
        start_frame = 0
        
        for i, is_voice in enumerate(voice_activity):
            if is_voice and not in_segment:
                start_frame = i
                in_segment = True
            elif not is_voice and in_segment:
                start_time = start_frame * hop_length / sample_rate
                end_time = i * hop_length / sample_rate
                if end_time - start_time > 0.5:  # Minimum 0.5s segment
                    segments.append({
                        'start': start_time,
                        'end': end_time,
                        'speaker': f'SPEAKER_{len(segments) % 3:02d}'  # Simulate multiple speakers
                    })
                in_segment = False
        
        logger.info(f"Found {len(segments)} voice segments")
        return segments
    
    def evaluate_voice_quality(self, audio_segment: np.ndarray, 
                               sample_rate: int) -> float:
        """
        Evaluate voice quality/smoothness of an audio segment
        
        Args:
            audio_segment: Audio samples for a segment
            sample_rate: Sample rate
            
        Returns:
            Quality score (higher is better)
        """
        # Calculate features that indicate voice quality
        
        # 1. Signal-to-noise ratio estimate
        energy = np.sqrt(np.mean(audio_segment ** 2))
        
        # 2. Zero crossing rate (lower is usually smoother for voice)
        zcr = np.mean(librosa.feature.zero_crossing_rate(audio_segment)[0])
        
        # 3. Spectral centroid (frequency center of mass)
        spectral_centroid = np.mean(
            librosa.feature.spectral_centroid(y=audio_segment, sr=sample_rate)[0]
        )
        
        # 4. Spectral rolloff (frequency below which 85% of energy is contained)
        spectral_rolloff = np.mean(
            librosa.feature.spectral_rolloff(y=audio_segment, sr=sample_rate)[0]
        )
        
        # Combined quality score (normalized)
        # Higher energy, lower ZCR, and moderate spectral features = better quality
        quality_score = (
            energy * 10 +  # Energy contribution
            (1 - zcr) * 5 +  # ZCR contribution (inverted)
            (1 / (1 + spectral_centroid / 1000)) * 3 +  # Spectral centroid
            (1 / (1 + spectral_rolloff / 1000)) * 2  # Spectral rolloff
        )
        
        logger.debug(f"Voice quality score: {quality_score:.4f}")
        return quality_score
    
    def select_best_voice(self, audio_data: np.ndarray, sample_rate: int,
                         segments: List[Dict]) -> Tuple[str, Dict]:
        """
        Select the best voice from multiple speakers
        
        Args:
            audio_data: Full audio data
            sample_rate: Sample rate
            segments: Speaker segments from diarization
            
        Returns:
            Tuple of (best_speaker_id, best_segment_info)
        """
        logger.info("Evaluating voice quality for each speaker")
        
        # Group segments by speaker
        speaker_segments = {}
        for seg in segments:
            speaker = seg['speaker']
            if speaker not in speaker_segments:
                speaker_segments[speaker] = []
            speaker_segments[speaker].append(seg)
        
        # Evaluate quality for each speaker
        speaker_scores = {}
        for speaker, segs in speaker_segments.items():
            scores = []
            for seg in segs[:3]:  # Evaluate first 3 segments max
                start_sample = int(seg['start'] * sample_rate)
                end_sample = int(seg['end'] * sample_rate)
                segment_audio = audio_data[start_sample:end_sample]
                
                if len(segment_audio) > 0:
                    score = self.evaluate_voice_quality(segment_audio, sample_rate)
                    scores.append(score)
            
            if scores:
                speaker_scores[speaker] = np.mean(scores)
        
        # Select best speaker
        best_speaker = max(speaker_scores.items(), key=lambda x: x[1])
        logger.info(f"Best speaker: {best_speaker[0]} with score {best_speaker[1]:.4f}")
        
        return best_speaker[0], speaker_segments[best_speaker[0]][0]
    
    def convert_voice(self, source_audio: np.ndarray, target_audio: np.ndarray,
                     sample_rate: int) -> np.ndarray:
        """
        Convert source voice to match target voice characteristics
        
        This is a simplified pitch/timbre shifting approach.
        For production use, implement proper voice conversion with neural networks.
        
        Args:
            source_audio: Source audio to convert
            target_audio: Target audio (reference voice)
            sample_rate: Sample rate
            
        Returns:
            Converted audio
        """
        logger.debug("Converting voice characteristics")
        
        # Extract pitch information
        source_f0 = librosa.yin(source_audio, 
                               fmin=librosa.note_to_hz('C2'),
                               fmax=librosa.note_to_hz('C7'),
                               sr=sample_rate)
        
        target_f0 = librosa.yin(target_audio,
                               fmin=librosa.note_to_hz('C2'),
                               fmax=librosa.note_to_hz('C7'),
                               sr=sample_rate)
        
        # Calculate average pitch shift needed
        source_f0_mean = np.mean(source_f0[source_f0 > 0])
        target_f0_mean = np.mean(target_f0[target_f0 > 0])
        
        if source_f0_mean > 0 and target_f0_mean > 0:
            pitch_shift = 12 * np.log2(target_f0_mean / source_f0_mean)
            pitch_shift = np.clip(pitch_shift, -5, 5)  # Limit shift range
        else:
            pitch_shift = 0
        
        # Apply pitch shift
        converted = librosa.effects.pitch_shift(source_audio, 
                                               sr=sample_rate,
                                               n_steps=pitch_shift)
        
        # Apply simple spectral envelope matching (via formant shifting approximation)
        # This is a very simplified approach
        converted = librosa.effects.preemphasis(converted, coef=0.97)
        
        return converted
    
    def process_audio_file(self, input_file: str, output_file: str,
                          progress_callback=None) -> bool:
        """
        Main processing pipeline
        
        Args:
            input_file: Input MP3 file path
            output_file: Output MP3 file path
            progress_callback: Callback function for progress updates (0-100)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Starting audio processing: {input_file}")
            
            if progress_callback:
                progress_callback(5, "Loading audio file...")
            
            # Load audio
            audio_data, sample_rate = self.load_audio(input_file)
            
            if progress_callback:
                progress_callback(15, "Performing speaker diarization...")
            
            # Perform diarization
            segments = self.perform_diarization(audio_data, sample_rate)
            
            if len(segments) == 0:
                logger.warning("No voice segments found")
                return False
            
            if progress_callback:
                progress_callback(30, "Selecting best voice...")
            
            # Select best voice
            best_speaker, best_segment = self.select_best_voice(
                audio_data, sample_rate, segments
            )
            
            # Get reference audio for best speaker
            ref_start = int(best_segment['start'] * sample_rate)
            ref_end = int(best_segment['end'] * sample_rate)
            reference_audio = audio_data[ref_start:ref_end]
            
            if progress_callback:
                progress_callback(45, "Converting other voices...")
            
            # Convert other speakers' voices
            output_audio = audio_data.copy()
            
            for i, seg in enumerate(segments):
                if seg['speaker'] != best_speaker:
                    start_sample = int(seg['start'] * sample_rate)
                    end_sample = int(seg['end'] * sample_rate)
                    segment_audio = audio_data[start_sample:end_sample]
                    
                    # Convert voice
                    converted = self.convert_voice(segment_audio, reference_audio, sample_rate)
                    output_audio[start_sample:end_sample] = converted
                    
                    # Update progress
                    if progress_callback:
                        progress = 45 + int(40 * (i + 1) / len(segments))
                        progress_callback(progress, f"Converting segment {i+1}/{len(segments)}...")
            
            if progress_callback:
                progress_callback(90, "Saving output file...")
            
            # Save output
            self.save_audio(output_audio, sample_rate, output_file, format="mp3")
            
            if progress_callback:
                progress_callback(100, "Processing complete!")
            
            logger.info("Audio processing completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error during audio processing: {e}", exc_info=True)
            if progress_callback:
                progress_callback(-1, f"Error: {str(e)}")
            return False
    
    def cleanup(self):
        """Clean up temporary files"""
        logger.info("Cleaning up temporary files")
        try:
            import shutil
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
            self.temp_dir.mkdir(exist_ok=True)
        except Exception as e:
            logger.warning(f"Error during cleanup: {e}")
