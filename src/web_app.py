"""
VoiceMix - Web Application V2
Flask-based web interface for source-target voice transfer
"""

import os
import logging
import secrets
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

# Global dictionary to track processing status
processing_status = {}
uploaded_files = {}  # Track uploaded source and target files
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


def transfer_voice_task(session_id, source_path, target_path, output_path):
    """Background task for voice transfer"""
    def progress_callback(progress, message):
        with processing_lock:
            processing_status[session_id] = {
                'progress': progress,
                'message': message,
                'status': 'processing'
            }
    
    try:
        logger.info(f"Starting voice transfer for session: {session_id}")
        processor = AudioProcessor()
        
        success = processor.transfer_voice(
            source_path,
            target_path,
            output_path,
            progress_callback=progress_callback
        )
        
        with processing_lock:
            if success:
                processing_status[session_id] = {
                    'progress': 100,
                    'message': 'Voice transfer complete!',
                    'status': 'complete',
                    'output_file': output_path
                }
            else:
                processing_status[session_id] = {
                    'progress': 0,
                    'message': 'Voice transfer failed',
                    'status': 'error'
                }
        
        processor.cleanup()
        logger.info(f"Voice transfer completed for session: {session_id}")
        
    except Exception as e:
        logger.error(f"Error during voice transfer for session {session_id}: {e}", exc_info=True)
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


@app.route('/upload_source', methods=['POST'])
def upload_source():
    """Handle source file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only MP3 files are allowed'}), 400
        
        session_id = get_session_id()
        
        # Save the source file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{session_id}_{timestamp}_source_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Store file info
        if session_id not in uploaded_files:
            uploaded_files[session_id] = {}
        
        uploaded_files[session_id]['source'] = {
            'path': file_path,
            'filename': filename
        }
        
        logger.info(f"Source file uploaded: {unique_filename}")
        
        return jsonify({
            'success': True,
            'message': 'Source file uploaded successfully',
            'filename': filename
        })
        
    except Exception as e:
        logger.error(f"Error uploading source file: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/upload_target', methods=['POST'])
def upload_target():
    """Handle target file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only MP3 files are allowed'}), 400
        
        session_id = get_session_id()
        
        # Save the target file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{session_id}_{timestamp}_target_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Store file info
        if session_id not in uploaded_files:
            uploaded_files[session_id] = {}
        
        uploaded_files[session_id]['target'] = {
            'path': file_path,
            'filename': filename
        }
        
        logger.info(f"Target file uploaded: {unique_filename}")
        
        return jsonify({
            'success': True,
            'message': 'Target file uploaded successfully',
            'filename': filename
        })
        
    except Exception as e:
        logger.error(f"Error uploading target file: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/transfer_voice', methods=['POST'])
def start_transfer():
    """Start voice transfer processing"""
    try:
        session_id = get_session_id()
        
        # Check if both files are uploaded
        if session_id not in uploaded_files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        files = uploaded_files[session_id]
        
        if 'source' not in files or 'target' not in files:
            return jsonify({'error': 'Both source and target files must be uploaded'}), 400
        
        source_path = files['source']['path']
        target_path = files['target']['path']
        
        # Generate output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"{session_id}_{timestamp}_transferred.mp3"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Initialize processing status
        with processing_lock:
            processing_status[session_id] = {
                'progress': 0,
                'message': 'Starting voice transfer...',
                'status': 'processing',
                'output_file': output_path
            }
        
        # Start processing in background thread
        thread = threading.Thread(
            target=transfer_voice_task,
            args=(session_id, source_path, target_path, output_path)
        )
        thread.daemon = True
        thread.start()
        
        logger.info(f"Voice transfer started for session: {session_id}")
        
        return jsonify({
            'success': True,
            'message': 'Voice transfer started'
        })
        
    except Exception as e:
        logger.error(f"Error starting voice transfer: {e}", exc_info=True)
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
        download_name='voicemix_transferred.mp3',
        mimetype='audio/mpeg'
    )


@app.route('/reset', methods=['POST'])
def reset_session():
    """Reset session"""
    session_id = get_session_id()
    
    with processing_lock:
        if session_id in processing_status:
            del processing_status[session_id]
        if session_id in uploaded_files:
            del uploaded_files[session_id]
    
    return jsonify({'success': True, 'message': 'Session reset'})


if __name__ == '__main__':
    logger.info("Starting VoiceMix Web Application V2")
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
