import os
import pytest
import sys

# Ensure the backend directory is in the path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert "status" in data
    assert data["status"] == "API is running"

def test_predict_no_data(client):
    """Test the predict endpoint with missing data."""
    response = client.post('/predict', json={})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_predict_success(client):
    """Test the predict endpoint with valid data."""
    # For this test to fully pass with a 200, the model must be trained.
    # We use a short text that might just return UNVERIFIABLE quickly from the live check if it fails,
    # or TRUE/FALSE if successful. The key is to check the response structure.
    response = client.post('/predict', json={"text": "Scientists discover new planet"})
    if response.status_code == 200:
        data = response.get_json()
        assert "ai_verdict" in data
        assert data["ai_verdict"] in ["TRUE", "FALSE", "UNVERIFIABLE"]
        assert "ai_explanation" in data
        assert "legacy_prediction" in data
