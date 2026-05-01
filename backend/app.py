import os
import pickle
import logging
import re
import requests
import urllib.parse
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) so the frontend can communicate with the backend
CORS(app)

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'fake_news_model.pkl')

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    logger.info("Model loaded successfully.")
except FileNotFoundError:
    logger.error("Model file not found. Please run train_model.py first.")
    model = None

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint to ensure API is running."""
    return jsonify({"status": "API is running", "model_loaded": model is not None}), 200

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)     # remove URLs
    text = re.sub(r"[^a-zA-Z ]", "", text)  # remove symbols
    return text

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint to predict if text is Real or Fake News."""
    if model is None:
        return jsonify({"error": "Model is not loaded on the server."}), 500

    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided. Please send JSON with a 'text' field."}), 400

        text = data['text'].strip()
        if not text:
            return jsonify({"error": "Empty text provided."}), 400

        # Legacy ML Model Prediction
        cleaned_input = clean_text(text)
        legacy_prediction = "Unknown"
        if model is not None:
            legacy_prediction = model.predict([cleaned_input])[0]
            
        # General AI Internet Check with LIVE WEB SCRAPING
        logger.info("Starting live internet search and AI fact-check...")
        context = ""
        
        # 1. Try fetching live news via DuckDuckGo
        try:
            from duckduckgo_search import DDGS
            news_results = DDGS().news(text, max_results=5)
            if news_results:
                context += "Live News Articles:\n"
                for res in news_results:
                    context += f"- {res['title']}: {res['body']}\n"
        except Exception as e:
            logger.warning(f"DuckDuckGo search failed: {e}")
            
        # 2. Try fetching Wikipedia for broader search context
        try:
            import wikipedia
            import warnings
            warnings.filterwarnings("ignore", category=UserWarning, module='wikipedia')
            
            # Broaden the search by extracting larger keyword terms if exact search fails
            search_results = wikipedia.search(text, results=2)
            if not search_results:
                keywords = " ".join([w for w in text.split() if len(w) > 3])
                search_results = wikipedia.search(keywords, results=2)
                
            if search_results:
                for page_title in search_results:
                    try:
                        summary = wikipedia.summary(page_title, sentences=3, auto_suggest=False)
                        context += f"\nWikipedia ({page_title}): {summary}\n"
                    except Exception:
                        pass
        except Exception as e:
            logger.warning(f"Wikipedia search failed: {e}")

        current_date = datetime.now().strftime("%B %d, %Y")
        prompt = f"Today is {current_date}. You are an advanced AI fact-checker connected to the live internet. Fact-check the user's statement. Here is the latest up-to-date internet context downloaded right now:\n{context}\n\nUser statement: '{text}'. Is it true or false? Start your response with exactly 'TRUE.', 'FALSE.', or 'UNVERIFIABLE.', followed by a clear explanation. IMPORTANT RULE: Never mention a 'knowledge cutoff', 'September 2023', or that you 'cannot search the internet', because you MUST act using the live internet context provided above to give the most up to date, 100% current answer."
        
        ai_verdict = "UNVERIFIABLE"
        ai_explanation = "Failed to reach the AI fact-checking server."
        
        try:
            url = "https://text.pollinations.ai/" + urllib.parse.quote(prompt) + "?model=openai"
            ai_response = requests.get(url, timeout=20).text.strip()
            
            # If the API returns JSON, extract the text content
            if ai_response.startswith('{'):
                import json
                try:
                    data = json.loads(ai_response)
                    if 'content' in data and data['content']:
                        ai_response = data['content']
                    elif 'reasoning' in data and data['reasoning']:
                        ai_response = data['reasoning']
                except Exception:
                    pass
            
            if ai_response.upper().startswith("TRUE"):
                ai_verdict = "TRUE"
            elif ai_response.upper().startswith("FALSE"):
                ai_verdict = "FALSE"
                
            ai_explanation = ai_response
        except Exception as e:
            logger.error(f"Pollinations AI request failed: {e}")

        response = {
            "text": text,
            "legacy_prediction": legacy_prediction,
            "ai_verdict": ai_verdict,
            "ai_explanation": ai_explanation
        }
        
        logger.info(f"Predicted '{ai_verdict}' for text: '{text[:30]}...'")
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return jsonify({"error": "An internal error occurred during prediction."}), 500

if __name__ == '__main__':
    # Use environment variable for port, or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Listen on all interfaces (0.0.0.0)
    app.run(host='0.0.0.0', port=port, debug=True)
