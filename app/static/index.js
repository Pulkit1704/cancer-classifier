document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const statusMessage = document.getElementById('statusMessage');
    const resultsContainer = document.getElementById('resultsContainer');
    const tableBody = document.querySelector('#resultsTable tbody');
    
    if (!fileInput.files[0]) return;

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    // Reset UI state
    resultsContainer.style.display = 'none';
    tableBody.innerHTML = ''; 
    statusMessage.textContent = 'Processing matrix and executing alignment...';
    statusMessage.style.color = '#555';

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server responded with status ${response.status}`);
        }

        const data = await response.json();
        
        // Normalize data to an array if it arrives as a single object
        const predictions = Array.isArray(data) ? data : [data];

        if (predictions.length === 0) {
            statusMessage.textContent = 'No predictions returned from the model.';
            return;
        }

        // Build and append table rows
        predictions.forEach(item => {
            const row = document.createElement('tr');
            
            const sampleId = item.sample_id || item.id || 'N/A';
            const prediction = item.prediction || item.class || 'N/A';
            const confidence = item.confidence !== undefined ? item.confidence : 'N/A';

            row.innerHTML = `
                <td><strong>${sampleId}</strong></td>
                <td>${prediction}</td>
                <td>${confidence}</td>
            `;
            tableBody.appendChild(row);
        });

        // Clear status text and show the populated table
        statusMessage.textContent = '';
        resultsContainer.style.display = 'block';

    } catch (error) {
        statusMessage.textContent = 'Inference failed: ' + error.message;
        statusMessage.style.color = '#dc3545'; // Highlight error in red
    }
});