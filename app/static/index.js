

document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const resultsDiv = document.getElementById('results');
    
    if (!fileInput.files[0]) return;

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    resultsDiv.style.display = 'block';
    resultsDiv.textContent = 'Processing matrix and executing alignment...';

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        resultsDiv.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        resultsDiv.textContent = 'Inference failed: ' + error.message;
    }
});