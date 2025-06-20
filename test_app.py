import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_root_route(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Shakespearean Insults' in resp.data

def test_insult_route(client):
    resp = client.get('/insult')
    assert resp.status_code == 200
    assert resp.data.strip() != b''

def test_audio_route(client):
    resp = client.get('/audio')
    assert resp.status_code == 200
    assert resp.mimetype == 'audio/mpeg'
    assert resp.headers.get('X-Insult-Text')
    assert resp.data  # Should not be empty

def test_cors_headers(client):
    resp = client.get('/insult')
    assert 'Access-Control-Allow-Origin' in resp.headers
