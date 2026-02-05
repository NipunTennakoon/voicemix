// VoiceMix V2 - Two-File Upload JavaScript

let sourceFile = null;
let targetFile = null;
let processingInterval = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    setupSourceUpload();
    setupTargetUpload();
});

// Source file upload setup
function setupSourceUpload() {
    const dropZone = document.getElementById('sourceDropZone');
    const fileInput = document.getElementById('sourceFileInput');
    
    // Click to browse
    dropZone.addEventListener('click', function(e) {
        if (e.target === dropZone || e.target.closest('.upload-zone')) {
            fileInput.click();
        }
    });
    
    // File input change
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleSourceFile(e.target.files[0]);
        }
    });
    
    // Drag and drop
    dropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add('drag-over');
    });
    
    dropZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('drag-over');
    });
    
    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('drag-over');
        
        if (e.dataTransfer.files.length > 0) {
            handleSourceFile(e.dataTransfer.files[0]);
        }
    });
}

// Target file upload setup
function setupTargetUpload() {
    const dropZone = document.getElementById('targetDropZone');
    const fileInput = document.getElementById('targetFileInput');
    
    // Click to browse
    dropZone.addEventListener('click', function(e) {
        if (e.target === dropZone || e.target.closest('.upload-zone')) {
            fileInput.click();
        }
    });
    
    // File input change
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleTargetFile(e.target.files[0]);
        }
    });
    
    // Drag and drop
    dropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add('drag-over');
    });
    
    dropZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('drag-over');
    });
    
    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('drag-over');
        
        if (e.dataTransfer.files.length > 0) {
            handleTargetFile(e.dataTransfer.files[0]);
        }
    });
}

// Handle source file
function handleSourceFile(file) {
    if (!file.name.toLowerCase().endsWith('.mp3')) {
        alert('Please select an MP3 file');
        return;
    }
    
    if (file.size > 500 * 1024 * 1024) {
        alert('File size exceeds 500MB limit');
        return;
    }
    
    sourceFile = file;
    
    // Show file info
    document.getElementById('sourceFileName').textContent = file.name;
    document.getElementById('sourceDropZone').style.display = 'none';
    document.getElementById('sourceFileInfo').style.display = 'block';
    
    // Set audio preview
    const audio = document.getElementById('sourceAudio');
    audio.src = URL.createObjectURL(file);
    
    // Upload file
    uploadSourceFile(file);
}

// Handle target file
function handleTargetFile(file) {
    if (!file.name.toLowerCase().endsWith('.mp3')) {
        alert('Please select an MP3 file');
        return;
    }
    
    if (file.size > 500 * 1024 * 1024) {
        alert('File size exceeds 500MB limit');
        return;
    }
    
    targetFile = file;
    
    // Show file info
    document.getElementById('targetFileName').textContent = file.name;
    document.getElementById('targetDropZone').style.display = 'none';
    document.getElementById('targetFileInfo').style.display = 'block';
    
    // Set audio preview
    const audio = document.getElementById('targetAudio');
    audio.src = URL.createObjectURL(file);
    
    // Upload file
    uploadTargetFile(file);
}

// Upload source file
function uploadSourceFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    fetch('/upload_source', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error uploading source file: ' + data.error);
            clearSource();
        } else {
            console.log('Source file uploaded successfully');
            checkTransferReady();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error uploading source file');
        clearSource();
    });
}

// Upload target file
function uploadTargetFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    fetch('/upload_target', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error uploading target file: ' + data.error);
            clearTarget();
        } else {
            console.log('Target file uploaded successfully');
            checkTransferReady();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error uploading target file');
        clearTarget();
    });
}

// Check if both files are uploaded
function checkTransferReady() {
    const transferBtn = document.getElementById('transferBtn');
    if (sourceFile && targetFile) {
        transferBtn.disabled = false;
    } else {
        transferBtn.disabled = true;
    }
}

// Clear source file
function clearSource() {
    sourceFile = null;
    document.getElementById('sourceDropZone').style.display = 'block';
    document.getElementById('sourceFileInfo').style.display = 'none';
    document.getElementById('sourceFileInput').value = '';
    checkTransferReady();
}

// Clear target file
function clearTarget() {
    targetFile = null;
    document.getElementById('targetDropZone').style.display = 'block';
    document.getElementById('targetFileInfo').style.display = 'none';
    document.getElementById('targetFileInput').value = '';
    checkTransferReady();
}

// Start voice transfer
function startTransfer() {
    if (!sourceFile || !targetFile) {
        alert('Please upload both source and target files');
        return;
    }
    
    // Disable button
    document.getElementById('transferBtn').disabled = true;
    
    // Show processing section
    document.getElementById('processingSection').style.display = 'block';
    
    // Start transfer
    fetch('/transfer_voice', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
            document.getElementById('processingSection').style.display = 'none';
            document.getElementById('transferBtn').disabled = false;
        } else {
            // Start polling for status
            startStatusPolling();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error starting voice transfer');
        document.getElementById('processingSection').style.display = 'none';
        document.getElementById('transferBtn').disabled = false;
    });
}

// Poll for processing status
function startStatusPolling() {
    processingInterval = setInterval(checkStatus, 1000);
}

function checkStatus() {
    fetch('/status')
    .then(response => response.json())
    .then(data => {
        const progress = data.progress || 0;
        const message = data.message || 'Processing...';
        const status = data.status;
        
        // Update progress bar
        const progressBar = document.getElementById('progressBar');
        progressBar.style.width = progress + '%';
        progressBar.textContent = progress + '%';
        
        // Update status message
        document.getElementById('statusMessage').textContent = message;
        
        // Check if complete
        if (status === 'complete') {
            clearInterval(processingInterval);
            showResults();
        } else if (status === 'error') {
            clearInterval(processingInterval);
            alert('Error: ' + message);
            document.getElementById('processingSection').style.display = 'none';
            document.getElementById('transferBtn').disabled = false;
        }
    })
    .catch(error => {
        console.error('Error checking status:', error);
    });
}

// Show results
function showResults() {
    document.getElementById('processingSection').style.display = 'none';
    document.getElementById('step4').style.display = 'block';
    
    // Set result audio source
    const resultAudio = document.getElementById('resultAudio');
    resultAudio.src = '/download';
    
    // Scroll to results
    document.getElementById('step4').scrollIntoView({ behavior: 'smooth' });
}

// Download file
function downloadFile() {
    window.location.href = '/download';
}

// Reset app
function resetApp() {
    // Clear files
    clearSource();
    clearTarget();
    
    // Hide sections
    document.getElementById('processingSection').style.display = 'none';
    document.getElementById('step4').style.display = 'none';
    
    // Reset progress
    document.getElementById('progressBar').style.width = '0%';
    document.getElementById('progressBar').textContent = '0%';
    
    // Reset session on server
    fetch('/reset', {
        method: 'POST'
    });
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
