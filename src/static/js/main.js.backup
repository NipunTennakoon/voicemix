// VoiceMix Web App JavaScript

let selectedFile = null;
let statusCheckInterval = null;

// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const uploadSection = document.getElementById('upload-section');
const processingSection = document.getElementById('processing-section');
const downloadSection = document.getElementById('download-section');
const errorSection = document.getElementById('error-section');
const progressBar = document.getElementById('progressBar');
const statusMessage = document.getElementById('statusMessage');
const errorMessage = document.getElementById('errorMessage');
const resetBtn = document.getElementById('resetBtn');
const resetErrorBtn = document.getElementById('resetErrorBtn');

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
    
    // Automatically start upload
    uploadFile();
}

// Upload file to server
function uploadFile() {
    if (!selectedFile) return;
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    // Show processing section
    processingSection.style.display = 'block';
    uploadSection.style.display = 'none';
    errorSection.style.display = 'none';
    downloadSection.style.display = 'none';
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showError(data.error);
        } else {
            // Start checking status
            startStatusCheck();
        }
    })
    .catch(error => {
        showError('Upload failed: ' + error.message);
    });
}

// Start checking processing status
function startStatusCheck() {
    statusCheckInterval = setInterval(checkStatus, 1000);
}

// Check processing status
function checkStatus() {
    fetch('/status')
    .then(response => response.json())
    .then(data => {
        updateProgress(data.progress, data.message);
        
        if (data.status === 'complete') {
            clearInterval(statusCheckInterval);
            showDownload();
        } else if (data.status === 'error') {
            clearInterval(statusCheckInterval);
            showError(data.message);
        }
    })
    .catch(error => {
        console.error('Status check failed:', error);
    });
}

// Update progress bar
function updateProgress(progress, message) {
    progressBar.style.width = progress + '%';
    progressBar.textContent = progress + '%';
    statusMessage.textContent = message;
}

// Show download section
function showDownload() {
    processingSection.style.display = 'none';
    downloadSection.style.display = 'block';
}

// Show error
function showError(message) {
    clearInterval(statusCheckInterval);
    processingSection.style.display = 'none';
    uploadSection.style.display = 'none';
    downloadSection.style.display = 'none';
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
        fileInput.value = '';
        fileInfo.style.display = 'none';
        uploadSection.style.display = 'block';
        processingSection.style.display = 'none';
        downloadSection.style.display = 'none';
        errorSection.style.display = 'none';
        progressBar.style.width = '0%';
        progressBar.textContent = '0%';
        statusMessage.textContent = 'Starting processing...';
    })
    .catch(error => {
        console.error('Reset failed:', error);
        location.reload();
    });
}

// Event listeners for reset buttons
resetBtn.addEventListener('click', resetApp);
resetErrorBtn.addEventListener('click', resetApp);
