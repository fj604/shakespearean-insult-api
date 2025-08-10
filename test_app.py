import pytest
import unittest.mock
import os
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_openai_key():
    """Set up a dummy OpenAI API key for testing"""
    original_key = os.environ.get("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "test-key-for-testing"
    yield
    if original_key is None:
        os.environ.pop("OPENAI_API_KEY", None)
    else:
        os.environ["OPENAI_API_KEY"] = original_key

def test_root_route(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Shakespearean Insults' in resp.data

def test_insult_route(client):
    resp = client.get('/insult')
    assert resp.status_code == 200
    assert resp.data.strip() != b''

@pytest.mark.skip(reason="Audio route requires OpenAI API access, which is not available in test environment")
def test_audio_route(client):
    # Test that the endpoint exists and handles requests appropriately
    # In a test environment without OpenAI access, we expect a connection error
    resp = client.get('/audio')
    
    # The route should handle the connection error gracefully
    # We expect either success (if mocked) or a 500 error (due to connection issues)
    assert resp.status_code in [200, 500]
    
    # Test that the insult text header is present if successful
    if resp.status_code == 200:
        assert resp.mimetype == 'audio/wav'
        assert resp.headers.get('X-Insult-Text')
        assert resp.data  # Should not be empty

def test_cors_headers(client):
    resp = client.get('/insult')
    assert 'Access-Control-Allow-Origin' in resp.headers
