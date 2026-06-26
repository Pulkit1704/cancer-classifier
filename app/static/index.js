const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const uploadContent = document.querySelector('.upload-content');
const fileInfo = document.getElementById('fileInfo');
const fileNameSpan = document.getElementById('fileName');
const removeFile = document.getElementById('removeFile');

const statusMessage = document.getElementById('statusMessage');
const resultsContainer = document.getElementById('resultsContainer');
const tableBody = document.querySelector('#resultsTable tbody');

// Handle Drag and Drop highlight styles
['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    }, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    }, false);
});

// Capture dropped files
dropZone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if(files.length) {
        fileInput.files = files;
        updateUIWithFile(files[0]);
    }
});

// Capture clicked files via file picker
fileInput.addEventListener('change', (e) => {
    if (fileInput.files.length) {
        updateUIWithFile(fileInput.files[0]);
    }
});

// Update UI to show selected file state
function updateUIWithFile(file) {
    uploadContent.style.display = 'none';
    fileNameSpan.textContent = file.name;
    fileInfo.style.display = 'inline-flex';
}

// Clear selected file configuration
removeFile.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation(); // Stop click from re-triggering file input selector
    fileInput.value = '';
    fileInfo.style.display = 'none';
    uploadContent.style.display = 'block';
});

// Form Submission handling
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!fileInput.files[0]) return;

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    // Reset UI state
    resultsContainer.style.display = 'none';
    tableBody.innerHTML = ''; 
    statusMessage.textContent = '🔬 Processing file and generating predictions...';
    statusMessage.style.background = '#f0f9ff';
    statusMessage.style.color = '#0369a1';

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server responded with status ${response.status}`);
        }

        const data = await response.json();
        const predictions = Array.isArray(data) ? data : [data];

        if (predictions.length === 0) {
            statusMessage.textContent = '⚠ No predictions returned from the model.';
            statusMessage.style.background = '#fffbeb';
            statusMessage.style.color = '#b45309';
            return;
        }

        predictions.forEach(item => {
            const row = document.createElement('tr');
            
            const sampleId = item.sample_id || item.id || 'N/A';
            const prediction = item.prediction || item.class || 'N/A';
            const confidence = item.confidence !== undefined ? item.confidence : 'N/A';

            row.innerHTML = `
                <td><strong>${sampleId}</strong></td>
                <td><span class="prediction-badge">${prediction}</span></td>
                <td>${confidence}</td>
            `;
            tableBody.appendChild(row);
        });

        statusMessage.textContent = '';
        statusMessage.style.background = 'transparent';
        resultsContainer.style.display = 'block';

    } catch (error) {
        statusMessage.textContent = '❌ Inference failed: ' + error.message;
        statusMessage.style.background = '#fef2f2';
        statusMessage.style.color = '#b91c1c';
    }
});