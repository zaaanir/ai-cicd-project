document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyze-btn');
    const newsText = document.getElementById('news-text');
    const resultSection = document.getElementById('result-section');
    const predictionBadge = document.getElementById('prediction-badge');
    const predictionText = document.getElementById('prediction-text');
    const loading = document.getElementById('loading');
    const errorMessage = document.getElementById('error-message');

    // When deploying, change this to your actual backend URL.
    // E.g., 'https://my-backend-app.onrender.com/predict'
    // You can also use an environment check if using a bundler, but for simple HTML/JS:
    const isLocalhost = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost' || window.location.hostname === '';
    
    // For Vercel/Render integration, if backend URL is known, replace it here.
    // We will leave it as localhost for now so it runs out-of-the-box locally.
    const API_URL = isLocalhost ? 'http://127.0.0.1:5000/predict' : 'https://ai-cicd-backend-production.up.railway.app/predict'; // Replace placeholder

    analyzeBtn.addEventListener('click', async () => {
        const text = newsText.value.trim();
        
        if (!text) {
            showError("Please enter some text to analyze.");
            return;
        }

        // UI state changes
        hideError();
        resultSection.classList.add('hidden');
        loading.classList.remove('hidden');
        analyzeBtn.disabled = true;

        try {
            // Wait an artificial 500ms to show loading animation (good for UX)
            await new Promise(resolve => setTimeout(resolve, 500));
            
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Something went wrong on the server.');
            }

            displayResult(data.ai_verdict, data.ai_explanation, data.legacy_prediction);
        } catch (error) {
            showError(`Error: ${error.message} - Ensure backend is running or update API_URL in script.js.`);
        } finally {
            loading.classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    });

    function displayResult(verdict, explanation, legacyScore) {
        // Reset classes
        predictionBadge.className = 'badge';
        
        if (verdict === 'TRUE') {
            predictionBadge.textContent = 'REAL NEWS (AI Verified)';
            predictionBadge.classList.add('real');
        } else if (verdict === 'FALSE') {
            predictionBadge.textContent = 'FAKE NEWS (AI Verified)';
            predictionBadge.classList.add('fake');
        } else {
            predictionBadge.textContent = 'UNVERIFIABLE';
            predictionBadge.classList.add('unverifiable');
        }

        predictionText.textContent = explanation || "No explanation provided.";
        document.getElementById('legacy-score').textContent = legacyScore || "Unknown";

        resultSection.classList.remove('hidden');
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('hidden');
    }

    function hideError() {
        errorMessage.classList.add('hidden');
        errorMessage.textContent = '';
    }
});
