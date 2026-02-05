#!/usr/bin/env python3
"""
Demonstration script to show the fix for "No voice segments detected" error
This script simulates the voice detection logic with various test cases
"""

import sys
from pathlib import Path

# Mock the dependencies to show the logic without requiring them
class MockLibrosa:
    class feature:
        @staticmethod
        def rms(y, frame_length, hop_length):
            # Simulate energy calculation
            import math
            n_frames = len(y) // hop_length
            energy = []
            for i in range(n_frames):
                start = i * hop_length
                end = min(start + frame_length, len(y))
                segment = y[start:end]
                rms = math.sqrt(sum(x**2 for x in segment) / len(segment)) if len(segment) > 0 else 0
                energy.append(rms)
            return [energy]

sys.modules['librosa'] = MockLibrosa()
sys.modules['librosa.feature'] = MockLibrosa.feature

import numpy as np

def perform_diarization_old(audio_data, sample_rate):
    """Old version that had the bug"""
    print("  OLD VERSION:")
    
    frame_length = int(0.025 * sample_rate)
    hop_length = int(0.010 * sample_rate)
    
    # Compute energy (simplified)
    energy = []
    for i in range(0, len(audio_data), hop_length):
        segment = audio_data[i:i+frame_length]
        if len(segment) > 0:
            rms = np.sqrt(np.mean(segment**2))
            energy.append(rms)
    energy = np.array(energy)
    
    # OLD: threshold too high
    threshold = np.mean(energy) * 0.5
    print(f"    Energy mean: {np.mean(energy):.6f}, threshold: {threshold:.6f}")
    voice_activity = energy > threshold
    
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
            if end_time - start_time > 0.5:  # OLD: minimum too high
                segments.append({
                    'start': start_time,
                    'end': end_time,
                    'speaker': f'SPEAKER_{len(segments):02d}'
                })
            in_segment = False
    
    # OLD: missing final segment handling
    print(f"    Segments found: {len(segments)}")
    return segments

def perform_diarization_new(audio_data, sample_rate):
    """New version with the fix"""
    print("  NEW VERSION:")
    
    if len(audio_data) == 0:
        print("    Empty audio data")
        return []
    
    frame_length = int(0.025 * sample_rate)
    hop_length = int(0.010 * sample_rate)
    
    # Ensure minimum frame length
    if frame_length < 1:
        frame_length = 512
    if hop_length < 1:
        hop_length = 256
    
    # Compute energy
    energy = []
    for i in range(0, len(audio_data), hop_length):
        segment = audio_data[i:i+frame_length]
        if len(segment) > 0:
            rms = np.sqrt(np.mean(segment**2))
            energy.append(rms)
    energy = np.array(energy)
    
    # NEW: Adaptive threshold using percentile
    if np.max(energy) > 0:
        threshold = np.percentile(energy, 25)
        threshold = max(threshold, np.max(energy) * 0.1)
    else:
        threshold = 0
    
    print(f"    Energy mean: {np.mean(energy):.6f}, max: {np.max(energy):.6f}, threshold: {threshold:.6f}")
    
    voice_activity = energy > threshold
    
    segments = []
    in_segment = False
    start_frame = 0
    min_segment_duration = 0.3  # NEW: reduced from 0.5s
    
    for i, is_voice in enumerate(voice_activity):
        if is_voice and not in_segment:
            start_frame = i
            in_segment = True
        elif not is_voice and in_segment:
            start_time = start_frame * hop_length / sample_rate
            end_time = i * hop_length / sample_rate
            if end_time - start_time > min_segment_duration:
                segments.append({
                    'start': start_time,
                    'end': end_time,
                    'speaker': f'SPEAKER_{len(segments):02d}'
                })
            in_segment = False
    
    # NEW: Handle final segment
    if in_segment:
        start_time = start_frame * hop_length / sample_rate
        end_time = len(audio_data) / sample_rate
        if end_time - start_time > min_segment_duration:
            segments.append({
                'start': start_time,
                'end': end_time,
                'speaker': f'SPEAKER_{len(segments):02d}'
            })
            print(f"    Added final segment extending to end")
    
    # NEW: Fallback for no segments
    if len(segments) == 0:
        print(f"    No segments detected, using entire audio as one segment")
        audio_duration = len(audio_data) / sample_rate
        if audio_duration > 0.1:
            segments.append({
                'start': 0.0,
                'end': audio_duration,
                'speaker': 'SPEAKER_00'
            })
    
    print(f"    Segments found: {len(segments)}")
    return segments

def test_case(name, audio_data, sample_rate):
    """Run a test case"""
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    print(f"  Audio duration: {len(audio_data) / sample_rate:.2f}s")
    print(f"  Audio amplitude range: [{np.min(audio_data):.3f}, {np.max(audio_data):.3f}]")
    
    old_segments = perform_diarization_old(audio_data, sample_rate)
    new_segments = perform_diarization_new(audio_data, sample_rate)
    
    if len(old_segments) == 0 and len(new_segments) > 0:
        print(f"\n  ✅ FIX SUCCESSFUL: Old version failed (0 segments), new version works ({len(new_segments)} segments)")
    elif len(old_segments) > 0 and len(new_segments) > 0:
        print(f"\n  ✓ Both versions work (old: {len(old_segments)}, new: {len(new_segments)} segments)")
    else:
        print(f"\n  ⚠ Results: old={len(old_segments)}, new={len(new_segments)}")

def main():
    """Run demonstration"""
    print("="*70)
    print("DEMONSTRATION: Fix for 'No voice segments detected' Error")
    print("="*70)
    
    sample_rate = 16000
    
    # Test 1: Quiet audio (common cause of the error)
    print("\n" + "="*70)
    print("Case 1: QUIET AUDIO")
    print("This is a common case that causes 'No voice segments detected'")
    duration = 2.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    quiet_audio = 0.05 * np.sin(2 * np.pi * 440 * t)  # Very quiet
    test_case("Quiet audio (amplitude 0.05)", quiet_audio, sample_rate)
    
    # Test 2: Short audio
    print("\n" + "="*70)
    print("Case 2: SHORT AUDIO")
    print("Short clips may not meet the 0.5s minimum duration in old version")
    duration = 0.4
    t = np.linspace(0, duration, int(sample_rate * duration))
    short_audio = np.sin(2 * np.pi * 440 * t)
    test_case("Short audio (0.4 seconds)", short_audio, sample_rate)
    
    # Test 3: Continuous speech (no pauses)
    print("\n" + "="*70)
    print("Case 3: CONTINUOUS AUDIO")
    print("Audio that extends to the end may lose the final segment in old version")
    duration = 2.5
    t = np.linspace(0, duration, int(sample_rate * duration))
    continuous_audio = np.sin(2 * np.pi * 440 * t)
    test_case("Continuous audio to end", continuous_audio, sample_rate)
    
    # Test 4: Very quiet background
    print("\n" + "="*70)
    print("Case 4: VERY LOW SNR")
    print("Audio with very low signal-to-noise ratio")
    duration = 1.5
    t = np.linspace(0, duration, int(sample_rate * duration))
    signal = 0.08 * np.sin(2 * np.pi * 440 * t)
    noise = 0.02 * np.random.randn(len(signal))
    low_snr_audio = signal + noise
    test_case("Low SNR audio", low_snr_audio.astype(np.float32), sample_rate)
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("""
The fix addresses several issues:

1. ✅ ADAPTIVE THRESHOLD: Uses percentile-based threshold instead of mean
   - More robust to varying audio levels
   - Works with quiet audio

2. ✅ LOWER MINIMUM DURATION: Reduced from 0.5s to 0.3s
   - Detects shorter speech segments
   - Works with brief utterances

3. ✅ FINAL SEGMENT HANDLING: Captures speech extending to end
   - No longer loses the last segment
   - Handles continuous speech

4. ✅ FALLBACK MECHANISM: Treats entire audio as one segment if nothing detected
   - Always returns at least one segment for valid audio
   - Prevents "No voice segments detected" error

The new version is much more robust and handles edge cases that previously
caused the "No voice segments detected" error.
""")

if __name__ == "__main__":
    main()
