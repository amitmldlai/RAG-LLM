document.getElementById('upload-form').onsubmit = async function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const uploadButton = document.getElementById('upload-button');

    uploadButton.textContent = 'Uploading...';
    uploadButton.disabled = true;

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const result = await response.json();
        uploadButton.textContent = 'Uploaded';
    } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
    } finally {
        uploadButton.disabled = false;
    }
};

document.getElementById('train-button').onclick = async function() {
    const trainType = document.getElementById('train-toggle').checked ? 'train_all' : 'train_latest';
    const apiUrl = 'http://127.0.0.1:5005/train'; // Update to your Flask server URL
    const trainButton = document.getElementById('train-button');

    trainButton.textContent = 'Training...';
    trainButton.disabled = true;

    const payload = {
        train_type: trainType
    };

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const result = await response.json();
        trainButton.textContent = 'Trained'; // Change text to 'Trained' when complete
    } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
    } finally {
        trainButton.disabled = false; // Re-enable the button
    }
};

document.getElementById('analyze-button').onclick = async function() {
    const button = this;
    button.textContent = 'Analyzing...'; // Change button text to "Analyzing"
    button.disabled = true; // Disable the button to prevent multiple clicks

    const apiUrl = 'http://127.0.0.1:5005/analyze'; // Update to your Flask server URL
    const query = document.getElementById('query-input').value;
    const searchType = document.querySelector('input[name="search-type"]:checked').value;

    const payload = {
        query: query,
        search_type: searchType
    };

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const arrayBuffer = await response.arrayBuffer();
        const text = new TextDecoder().decode(arrayBuffer);
        document.getElementById('response-output').value = text;

        button.textContent = 'Analyzed'; // Change button text to "Analyzed"
    } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
        button.textContent = 'Analyze'; // Reset button text on error
    } finally {
        button.disabled = false; // Re-enable the button after the operation
    }
};

document.getElementById('train-toggle').onchange = function() {
    const label = document.getElementById('train-label');
    label.textContent = this.checked ? 'Train All' : 'Train Latest';
};
