"""
VoiceMix - Web Application
Flask-based web interface for MP3 voice processing
"""

import os
import logging
import secrets
import json
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
import threading

from audio_processor import AudioProcessor

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('voicemix_web.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['ALLOWED_EXTENSIONS'] = {'mp3'}

# Create necessary directories
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(exist_ok=True)
Path('voice_clips').mkdir(exist_ok=True)

# Global dictionary to track processing status and voice data
processing_status = {}
voice_data = {}  # Store extracted voice information per session
processing_lock = threading.Lock()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def get_session_id():
    """Get or create session ID"""
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)
    return session['session_id']


def process_audio_task(session_id, input_path, output_path):
    """Background task for audio processing"""
    def progress_callback(progress, message):
        with processing_lock:
            processing_status[session_id] = {
                'progress': progress,
                'message': message,
                'status': 'processing'
            }
    
    try:
        logger.info(f"Starting processing for session: {session_id}")
        processor = AudioProcessor()
        
        success = processor.process_audio_file(
            input_path,
            output_path,
            progress_callback=progress_callback
        )
        
        with processing_lock:
            if success:
                processing_status[session_id] = {
                    'progress': 100,
                    'message': 'Processing complete!',
                    'status': 'complete',
                    'output_file': output_path
                }
            else:
                processing_status[session_id] = {
                    'progress': 0,
                    'message': 'Processing failed',
                    'status': 'error'
                }
        
        processor.cleanup()
        logger.info(f"Processing completed for session: {session_id}")
        
    except Exception as e:
        logger.error(f"Error processing audio for session {session_id}: {e}", exc_info=True)
        with processing_lock:
            processing_status[session_id] = {
                'progress': 0,
                'message': f'Error: {str(e)}',
                'status': 'error'
            }


@app.route('/')
def index():
    """Render the main dashboard page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if filename is empty
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only MP3 files are allowed'}), 400
        
        # Get or create session ID
        session_id = get_session_id()
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{session_id}_{timestamp}_{filename}"
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(input_path)
        
        # Generate output filename
        output_filename = f"{session_id}_{timestamp}_unified.mp3"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Initialize processing status
        with processing_lock:
            processing_status[session_id] = {
                'progress': 0,
                'message': 'Starting processing...',
                'status': 'processing',
                'input_file': input_path,
                'output_file': output_path
            }
        
        # Start processing in background thread
        thread = threading.Thread(
            target=process_audio_task,
            args=(session_id, input_path, output_path)
        )
        thread.daemon = True
        thread.start()
        
        logger.info(f"File uploaded and processing started: {unique_filename}")
        
        return jsonify({
            'success': True,
            'message': 'File uploaded successfully. Processing started.',
            'session_id': session_id
        })
        
    except Exception as e:
        logger.error(f"Error uploading file: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/status')
def get_status():
    """Get processing status"""
    session_id = get_session_id()
    
    with processing_lock:
        status = processing_status.get(session_id, {
            'progress': 0,
            'message': 'No processing started',
            'status': 'idle'
        })
    
    return jsonify(status)


@app.route('/download')
def download_file():
    """Download processed file"""
    session_id = get_session_id()
    
    with processing_lock:
        status = processing_status.get(session_id)
    
    if not status or status.get('status') != 'complete':
        return jsonify({'error': 'No file available for download'}), 404
    
    output_file = status.get('output_file')
    
    if not output_file or not os.path.exists(output_file):
        return jsonify({'error': 'Output file not found'}), 404
    
    return send_file(
        output_file,
        as_attachment=True,
        download_name='voicemix_unified.mp3',
        mimetype='audio/mpeg'
    )


def extract_voices_task(session_id, input_path):
    """Background task for voice extraction"""
    def progress_callback(progress, message):
        with processing_lock:
            processing_status[session_id] = {
                'progress': progress,
                'message': message,
                'status': 'analyzing'
            }
    
    try:
        logger.info(f"Starting voice extraction for session: {session_id}")
        processor = AudioProcessor()
        
        # Create output directory for this session
        voice_clips_dir = os.path.join('voice_clips', session_id)
        Path(voice_clips_dir).mkdir(exist_ok=True, parents=True)
        
        # Extract voice segments
        result = processor.extract_voice_segments(
            input_path,
            voice_clips_dir,
            progress_callback=progress_callback
        )
        
        with processing_lock:
            if result.get('speakers'):
                voice_data[session_id] = result
                processing_status[session_id] = {
                    'progress': 100,
                    'message': f'Found {len(result["speakers"])} unique voices!',
                    'status': 'voices_extracted',
                    'voice_count': len(result['speakers'])
                }
            else:
                processing_status[session_id] = {
                    'progress': 0,
                    'message': result.get('error', 'Voice extraction failed'),
                    'status': 'error'
                }
        
        logger.info(f"Voice extraction completed for session: {session_id}")
        
    except Exception as e:
        logger.error(f"Error extracting voices for session {session_id}: {e}", exc_info=True)
        with processing_lock:
            processing_status[session_id] = {
                'progress': 0,
                'message': f'Error: {str(e)}',
                'status': 'error'
            }


@app.route('/analyze', methods=['POST'])
def analyze_voices():
    """Analyze uploaded file and extract individual voices"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only MP3 files are allowed'}), 400
        
        # Get or create session ID
        session_id = get_session_id()
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{session_id}_{timestamp}_{filename}"
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(input_path)
        
        # Initialize status
        with processing_lock:
            processing_status[session_id] = {
                'progress': 0,
                'message': 'Starting voice analysis...',
                'status': 'analyzing',
                'input_file': input_path
            }
        
        # Start voice extraction in background thread
        thread = threading.Thread(
            target=extract_voices_task,
            args=(session_id, input_path)
        )
        thread.daemon = True
        thread.start()
        
        logger.info(f"File uploaded for analysis: {unique_filename}")
        
        return jsonify({
            'success': True,
            'message': 'File uploaded. Analyzing voices...',
            'session_id': session_id
        })
        
    except Exception as e:
        logger.error(f"Error analyzing file: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/get_voices')
def get_voices():
    """Get extracted voice clips for the session"""
    session_id = get_session_id()
    
    with processing_lock:
        data = voice_data.get(session_id)
    
    if not data:
        return jsonify({'error': 'No voice data available'}), 404
    
    # Prepare response with relative paths for download
    voices = []
    for speaker in data.get('speakers', []):
        voices.append({
            'id': speaker['id'],
            'clip_filename': speaker['clip_filename'],
            'duration': speaker['duration'],
            'quality_score': speaker['quality_score'],
            'segment_count': speaker['segment_count']
        })
    
    return jsonify({
        'voices': voices,
        'total_speakers': data.get('total_speakers', 0)
    })


@app.route('/download_voice/<int:voice_id>')
def download_voice_clip(voice_id):
    """Download a specific voice clip"""
    session_id = get_session_id()
    
    with processing_lock:
        data = voice_data.get(session_id)
    
    if not data:
        return jsonify({'error': 'No voice data available'}), 404
    
    # Find the requested voice
    voice = None
    for speaker in data.get('speakers', []):
        if speaker['id'] == voice_id:
            voice = speaker
            break
    
    if not voice:
        return jsonify({'error': 'Voice not found'}), 404
    
    clip_path = voice['clip_path']
    
    if not os.path.exists(clip_path):
        return jsonify({'error': 'Clip file not found'}), 404
    
    return send_file(
        clip_path,
        as_attachment=True,
        download_name=f'voice_{voice_id}.mp3',
        mimetype='audio/mpeg'
    )


def convert_voices_task(session_id, selected_voice_id):
    """Background task for voice conversion"""
    def progress_callback(progress, message):
        with processing_lock:
            processing_status[session_id]['progress'] = progress
            processing_status[session_id]['message'] = message
    
    try:
        logger.info(f"Starting voice conversion for session: {session_id}, voice: {selected_voice_id}")
        
        with processing_lock:
            data = voice_data.get(session_id)
        
        if not data:
            raise ValueError("No voice data found")
        
        # Find selected speaker
        selected_speaker = None
        for speaker in data['speakers']:
            if speaker['id'] == selected_voice_id:
                selected_speaker = speaker
                break
        
        if not selected_speaker:
            raise ValueError(f"Voice {selected_voice_id} not found")
        
        processor = AudioProcessor()
        
        # Create output directory for converted clips
        converted_dir = os.path.join('voice_clips', session_id, 'converted')
        Path(converted_dir).mkdir(exist_ok=True, parents=True)
        
        # Get all segments
        all_segments = []
        for speaker in data['speakers']:
            all_segments.extend(speaker['all_segments'])
        
        # Convert voices
        converted_clips = processor.convert_to_selected_voice(
            data['audio_data'],
            data['sample_rate'],
            all_segments,
            selected_speaker['speaker_id'],
            converted_dir,
            progress_callback=progress_callback
        )
        
        with processing_lock:
            processing_status[session_id] = {
                'progress': 100,
                'message': 'Voice conversion complete!',
                'status': 'converted',
                'selected_voice': selected_voice_id,
                'converted_clips': converted_clips
            }
        
        logger.info(f"Voice conversion completed for session: {session_id}")
        
    except Exception as e:
        logger.error(f"Error converting voices for session {session_id}: {e}", exc_info=True)
        with processing_lock:
            processing_status[session_id] = {
                'progress': 0,
                'message': f'Error: {str(e)}',
                'status': 'error'
            }


@app.route('/select_voice', methods=['POST'])
def select_voice():
    """Select a voice and convert others to match it"""
    try:
        data = request.get_json()
        voice_id = data.get('voice_id')
        
        if not voice_id:
            return jsonify({'error': 'No voice ID provided'}), 400
        
        session_id = get_session_id()
        
        # Check if voice data exists
        with processing_lock:
            if session_id not in voice_data:
                return jsonify({'error': 'No voice data available'}), 404
        
        # Initialize status for conversion
        with processing_lock:
            processing_status[session_id] = {
                'progress': 0,
                'message': 'Starting voice conversion...',
                'status': 'converting'
            }
        
        # Start conversion in background thread
        thread = threading.Thread(
            target=convert_voices_task,
            args=(session_id, voice_id)
        )
        thread.daemon = True
        thread.start()
        
        logger.info(f"Voice {voice_id} selected for session: {session_id}")
        
        return jsonify({
            'success': True,
            'message': 'Converting other voices to match selected voice...'
        })
        
    except Exception as e:
        logger.error(f"Error selecting voice: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/get_converted_clips')
def get_converted_clips():
    """Get list of converted voice clips"""
    session_id = get_session_id()
    
    with processing_lock:
        status = processing_status.get(session_id)
    
    if not status or status.get('status') != 'converted':
        return jsonify({'error': 'No converted clips available'}), 404
    
    converted_clips = status.get('converted_clips', [])
    
    return jsonify({
        'clips': converted_clips,
        'selected_voice': status.get('selected_voice')
    })


@app.route('/download_converted/<path:filename>')
def download_converted_clip(filename):
    """Download a converted voice clip"""
    session_id = get_session_id()
    
    converted_dir = os.path.join('voice_clips', session_id, 'converted')
    file_path = os.path.join(converted_dir, filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
        mimetype='audio/mpeg'
    )


@app.route('/reset')
def reset_session():
    """Reset the current session"""
    session_id = get_session_id()
    
    # Clean up old files
    with processing_lock:
        if session_id in processing_status:
            status = processing_status[session_id]
            if 'input_file' in status and os.path.exists(status['input_file']):
                try:
                    os.remove(status['input_file'])
                except:
                    pass
            if 'output_file' in status and os.path.exists(status['output_file']):
                try:
                    os.remove(status['output_file'])
                except:
                    pass
            del processing_status[session_id]
    
    # Create new session
    session.pop('session_id', None)
    
    return jsonify({'success': True, 'message': 'Session reset'})


if __name__ == '__main__':
    logger.info("Starting VoiceMix Web Application")
    app.run(host='0.0.0.0', port=5000, debug=True)
