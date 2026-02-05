"""
VoiceMix Web Application - Demo Mode
Simple demonstration of the web interface without audio processing
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

# Global status for demo
demo_status = {
    'progress': 0,
    'message': 'Ready',
    'status': 'idle'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def simulate_processing():
    """Simulate audio processing with progress updates"""
    global demo_status
    
    steps = [
        (5, "Loading audio file..."),
        (15, "Performing speaker diarization..."),
        (30, "Identifying speakers..."),
        (45, "Evaluating voice quality..."),
        (60, "Converting voices..."),
        (75, "Converting segment 1/3..."),
        (85, "Converting segment 2/3..."),
        (95, "Converting segment 3/3..."),
        (100, "Processing complete!")
    ]
    
    for progress, message in steps:
        time.sleep(1)  # Simulate work
        demo_status['progress'] = progress
        demo_status['message'] = message
        demo_status['status'] = 'processing'
    
    demo_status['status'] = 'complete'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
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
    
    # Reset and start demo processing
    demo_status = {
        'progress': 0,
        'message': 'Starting processing...',
        'status': 'processing'
    }
    
    thread = threading.Thread(target=simulate_processing)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'File uploaded successfully. Processing started.'
    })

@app.route('/status')
def get_status():
    return jsonify(demo_status)

@app.route('/download')
def download_file():
    # In demo mode, just return a message
    return jsonify({
        'message': 'Demo mode: In production, processed file would be downloaded here'
    })

@app.route('/reset')
def reset_session():
    global demo_status
    demo_status = {
        'progress': 0,
        'message': 'Ready',
        'status': 'idle'
    }
    return jsonify({'success': True, 'message': 'Session reset'})

if __name__ == '__main__':
    print("="*60)
    print("VoiceMix Web Application - DEMO MODE")
    print("="*60)
    print("")
    print("Access the dashboard at: http://localhost:5000")
    print("")
    print("This is a demo showing the web interface.")
    print("Audio processing is simulated (not actual processing).")
    print("")
    app.run(host='0.0.0.0', port=5000, debug=False)
