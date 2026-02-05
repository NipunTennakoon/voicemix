// VoiceMix Web App JavaScript - Enhanced with Voice Selection

let selectedFile = null;
let statusCheckInterval = null;
let selectedVoiceId = null;

// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');

const uploadSection = document.getElementById('upload-section');
const analyzingSection = document.getElementById('analyzing-section');
const voiceSelectionSection = document.getElementById('voice-selection-section');
const convertingSection = document.getElementById('converting-section');
const resultsSection = document.getElementById('results-section');
const errorSection = document.getElementById('error-section');

const analyzeProgressBar = document.getElementById('analyzeProgressBar');
const analyzeStatusMessage = document.getElementById('analyzeStatusMessage');
const convertProgressBar = document.getElementById('convertProgressBar');
const convertStatusMessage = document.getElementById('convertStatusMessage');

const errorMessage = document.getElementById('errorMessage');
const resetErrorBtn = document.getElementById('resetErrorBtn');
const processAnotherBtn = document.getElementById('processAnotherBtn');

// Prevent default drag behaviors
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Highlight drop zone when dragging over it
['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
        dropZone.classList.add('drag-over');
    }, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
        dropZone.classList.remove('drag-over');
    }, false);
});

// Handle dropped files
dropZone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}, false);

// Handle click on drop zone
dropZone.addEventListener('click', () => {
    fileInput.click();
});

// Handle file selection from input
fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

// Handle files
function handleFiles(files) {
    if (files.length === 0) return;
    
    const file = files[0];
    
    // Validate file type
    if (!file.name.toLowerCase().endsWith('.mp3')) {
        showError('Please select an MP3 file');
        return;
    }
    
    // Validate file size (500 MB)
    if (file.size > 500 * 1024 * 1024) {
        showError('File size exceeds 500 MB limit');
        return;
    }
    
    selectedFile = file;
    fileName.textContent = file.name;
    fileInfo.style.display = 'block';
    
    // Automatically start analysis
    analyzeFile();
}

// Analyze file and extract voices
function analyzeFile() {
    if (!selectedFile) return;
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    // Show analyzing section
    analyzingSection.style.display = 'block';
    uploadSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showError(data.error);
        } else {
            // Start checking status for voice extraction
            startStatusCheck('analyzing');
        }
    })
    .catch(error => {
        showError('Upload failed: ' + error.message);
    });
}

// Start checking processing status
function startStatusCheck(stage) {
    statusCheckInterval = setInterval(() => checkStatus(stage), 1000);
}

// Check processing status
function checkStatus(stage) {
    fetch('/status')
    .then(response => response.json())
    .then(data => {
        if (stage === 'analyzing') {
            updateAnalyzeProgress(data.progress, data.message);
            
            if (data.status === 'voices_extracted') {
                clearInterval(statusCheckInterval);
                loadVoices();
            } else if (data.status === 'error') {
                clearInterval(statusCheckInterval);
                showError(data.message);
            }
        } else if (stage === 'converting') {
            updateConvertProgress(data.progress, data.message);
            
            if (data.status === 'converted') {
                clearInterval(statusCheckInterval);
                showResults();
            } else if (data.status === 'error') {
                clearInterval(statusCheckInterval);
                showError(data.message);
            }
        }
    })
    .catch(error => {
        console.error('Status check failed:', error);
    });
}

// Update analyze progress bar
function updateAnalyzeProgress(progress, message) {
    analyzeProgressBar.style.width = progress + '%';
    analyzeProgressBar.textContent = progress + '%';
    analyzeStatusMessage.textContent = message;
}

// Update convert progress bar
function updateConvertProgress(progress, message) {
    convertProgressBar.style.width = progress + '%';
    convertProgressBar.textContent = progress + '%';
    convertStatusMessage.textContent = message;
}

// Load extracted voices
function loadVoices() {
    fetch('/get_voices')
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showError(data.error);
            return;
        }
        
        displayVoices(data.voices, data.total_speakers);
    })
    .catch(error => {
        showError('Failed to load voices: ' + error.message);
    });
}

// Display voice clips for selection
function displayVoices(voices, totalSpeakers) {
    analyzingSection.style.display = 'none';
    voiceSelectionSection.style.display = 'block';
    
    document.getElementById('voiceCount').textContent = totalSpeakers;
    
    const container = document.getElementById('voiceClipsContainer');
    container.innerHTML = '';
    
    voices.forEach(voice => {
        const col = document.createElement('div');
        col.className = 'col-md-6 mb-4';
        
        const card = document.createElement('div');
        card.className = 'card voice-card';
        card.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">
                    <i class="fas fa-microphone"></i> Voice ${voice.id}
                </h5>
                <div class="mb-3">
                    <audio controls class="w-100" id="audio-${voice.id}">
                        <source src="/download_voice/${voice.id}" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>
                </div>
                <div class="voice-info mb-3">
                    <small class="text-muted">
                        <i class="fas fa-clock"></i> Duration: ${voice.duration.toFixed(2)}s &nbsp;
                        <i class="fas fa-star"></i> Quality: ${voice.quality_score.toFixed(2)}
                    </small>
                </div>
                <button class="btn btn-primary w-100 select-voice-btn" data-voice-id="${voice.id}">
                    <i class="fas fa-check-circle"></i> Select This Voice
                </button>
            </div>
        `;
        
        col.appendChild(card);
        container.appendChild(col);
    });
    
    // Add event listeners to select buttons
    document.querySelectorAll('.select-voice-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const voiceId = parseInt(this.dataset.voiceId);
            selectVoice(voiceId);
        });
    });
}

// Select a voice and start conversion
function selectVoice(voiceId) {
    selectedVoiceId = voiceId;
    
    // Highlight selected voice
    document.querySelectorAll('.voice-card').forEach(card => {
        card.classList.remove('selected');
    });
    event.target.closest('.voice-card').classList.add('selected');
    
    // Show converting section
    voiceSelectionSection.style.display = 'none';
    convertingSection.style.display = 'block';
    
    // Start conversion
    fetch('/select_voice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ voice_id: voiceId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showError(data.error);
        } else {
            // Start checking conversion status
            startStatusCheck('converting');
        }
    })
    .catch(error => {
        showError('Voice selection failed: ' + error.message);
    });
}

// Show results with converted clips
function showResults() {
    fetch('/get_converted_clips')
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showError(data.error);
            return;
        }
        
        displayConvertedClips(data.clips, data.selected_voice);
    })
    .catch(error => {
        showError('Failed to load results: ' + error.message);
    });
}

// Display converted clips for download
function displayConvertedClips(clips, selectedVoice) {
    convertingSection.style.display = 'none';
    resultsSection.style.display = 'block';
    
    const container = document.getElementById('convertedClipsContainer');
    container.innerHTML = '';
    
    // Add info about selected voice
    const info = document.createElement('div');
    info.className = 'col-12 mb-4';
    info.innerHTML = `
        <div class="alert alert-info">
            <i class="fas fa-info-circle"></i> <strong>Selected Voice:</strong> Voice ${selectedVoice}
            <br>All other voices have been converted to match this voice.
        </div>
    `;
    container.appendChild(info);
    
    // Display each converted clip
    clips.forEach((clip, index) => {
        const col = document.createElement('div');
        col.className = 'col-md-6 mb-3';
        
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <div class="card-body">
                <h6 class="card-title">
                    <i class="fas fa-file-audio"></i> Converted Clip ${index + 1}
                </h6>
                <div class="mb-3">
                    <audio controls class="w-100">
                        <source src="/download_converted/${clip.clip_filename}" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>
                </div>
                <small class="text-muted d-block mb-2">
                    <i class="fas fa-clock"></i> Duration: ${clip.duration.toFixed(2)}s
                </small>
                <a href="/download_converted/${clip.clip_filename}" 
                   class="btn btn-success btn-sm w-100" download>
                    <i class="fas fa-download"></i> Download
                </a>
            </div>
        `;
        
        col.appendChild(card);
        container.appendChild(col);
    });
}

// Show error
function showError(message) {
    clearInterval(statusCheckInterval);
    uploadSection.style.display = 'none';
    analyzingSection.style.display = 'none';
    voiceSelectionSection.style.display = 'none';
    convertingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'block';
    errorMessage.textContent = message;
}

// Reset and start over
function resetApp() {
    fetch('/reset')
    .then(response => response.json())
    .then(data => {
        // Reset UI
        selectedFile = null;
        selectedVoiceId = null;
        fileInput.value = '';
        fileInfo.style.display = 'none';
        uploadSection.style.display = 'block';
        analyzingSection.style.display = 'none';
        voiceSelectionSection.style.display = 'none';
        convertingSection.style.display = 'none';
        resultsSection.style.display = 'none';
        errorSection.style.display = 'none';
        
        analyzeProgressBar.style.width = '0%';
        analyzeProgressBar.textContent = '0%';
        convertProgressBar.style.width = '0%';
        convertProgressBar.textContent = '0%';
    })
    .catch(error => {
        console.error('Reset failed:', error);
        location.reload();
    });
}

// Event listeners for reset buttons
resetErrorBtn.addEventListener('click', resetApp);
processAnotherBtn.addEventListener('click', resetApp);
