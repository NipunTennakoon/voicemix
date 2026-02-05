"""
VoiceMix Web Application - Demo Mode with Voice Selection
Demonstration of the enhanced voice selection interface
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import time
import threading
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'demo_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp3'}

Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path('voice_clips').mkdir(exist_ok=True)

# Global status for demo
demo_status = {
    'progress': 0,
    'message': 'Ready',
    'status': 'idle'
}

demo_voices = []
demo_converted_clips = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def simulate_voice_extraction():
    """Simulate voice extraction with progress updates"""
    global demo_status, demo_voices
    
    steps = [
        (10, "Loading audio file..."),
        (30, "Performing speaker diarization..."),
        (50, "Identifying speakers..."),
        (70, "Extracting voice 1..."),
        (85, "Extracting voice 2..."),
        (100, "Found 3 unique voices!")
    ]
    
    for progress, message in steps:
        time.sleep(0.5)
        demo_status['progress'] = progress
        demo_status['message'] = message
        demo_status['status'] = 'analyzing'
    
    # Simulate 3 voices found
    demo_voices = [
        {'id': 1, 'clip_filename': 'voice_1.mp3', 'duration': 1.5, 'quality_score': 8.5, 'segment_count': 2},
        {'id': 2, 'clip_filename': 'voice_2.mp3', 'duration': 0.8, 'quality_score': 7.2, 'segment_count': 1},
        {'id': 3, 'clip_filename': 'voice_3.mp3', 'duration': 1.2, 'quality_score': 6.8, 'segment_count': 1}
    ]
    
    demo_status['status'] = 'voices_extracted'
    demo_status['voice_count'] = 3

def simulate_voice_conversion(selected_voice):
    """Simulate voice conversion with progress updates"""
    global demo_status, demo_converted_clips
    
    demo_status['status'] = 'converting'
    
    steps = [
        (20, "Converting voice 2..."),
        (60, "Converting voice 3..."),
        (100, "Voice conversion complete!")
    ]
    
    for progress, message in steps:
        time.sleep(0.5)
        demo_status['progress'] = progress
        demo_status['message'] = message
    
    # Simulate converted clips (excluding the selected voice)
    demo_converted_clips = []
    for voice in demo_voices:
        if voice['id'] != selected_voice:
            demo_converted_clips.append({
                'original_speaker': f"SPEAKER_{voice['id']}",
                'clip_filename': f"converted_voice_SPEAKER_{voice['id']}.mp3",
                'duration': voice['duration']
            })
    
    demo_status['status'] = 'converted'
    demo_status['selected_voice'] = selected_voice

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_voices():
    global demo_status
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only MP3 files are allowed'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Reset and start demo analysis
    demo_status = {
        'progress': 0,
        'message': 'Starting voice analysis...',
        'status': 'analyzing'
    }
    
    thread = threading.Thread(target=simulate_voice_extraction)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'File uploaded. Analyzing voices...'
    })

@app.route('/status')
def get_status():
    return jsonify(demo_status)

@app.route('/get_voices')
def get_voices():
    return jsonify({
        'voices': demo_voices,
        'total_speakers': len(demo_voices)
    })

@app.route('/download_voice/<int:voice_id>')
def download_voice_clip(voice_id):
    return jsonify({
        'message': f'Demo mode: Voice {voice_id} clip download'
    })

@app.route('/select_voice', methods=['POST'])
def select_voice():
    data = request.get_json()
    voice_id = data.get('voice_id')
    
    if not voice_id:
        return jsonify({'error': 'No voice ID provided'}), 400
    
    global demo_status
    demo_status = {
        'progress': 0,
        'message': 'Starting voice conversion...',
        'status': 'converting'
    }
    
    thread = threading.Thread(target=simulate_voice_conversion, args=(voice_id,))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Converting other voices to match selected voice...'
    })

@app.route('/get_converted_clips')
def get_converted_clips():
    return jsonify({
        'clips': demo_converted_clips,
        'selected_voice': demo_status.get('selected_voice', 1)
    })

@app.route('/download_converted/<path:filename>')
def download_converted_clip(filename):
    return jsonify({
        'message': f'Demo mode: Download {filename}'
    })

@app.route('/reset')
def reset_session():
    global demo_status, demo_voices, demo_converted_clips
    demo_status = {
        'progress': 0,
        'message': 'Ready',
        'status': 'idle'
    }
    demo_voices = []
    demo_converted_clips = []
    return jsonify({'success': True, 'message': 'Session reset'})

if __name__ == '__main__':
    print("="*60)
    print("VoiceMix Web Application - DEMO MODE (Enhanced)")
    print("="*60)
    print("")
    print("Access the dashboard at: http://localhost:5000")
    print("")
    print("This demo shows the enhanced voice selection workflow.")
    print("Audio processing is simulated.")
    print("")
    app.run(host='0.0.0.0', port=5000, debug=False)
