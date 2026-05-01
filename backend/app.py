import os
import pickle
import logging
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

        # Make prediction
        prediction = model.predict([text])[0]
        
        response = {
            "text": text,
            "prediction": prediction
        }
        
        logger.info(f"Predicted '{prediction}' for text: '{text[:30]}...'")
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return jsonify({"error": "An internal error occurred during prediction."}), 500

if __name__ == '__main__':
    # Use environment variable for port, or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Listen on all interfaces (0.0.0.0)
    app.run(host='0.0.0.0', port=port, debug=True)
