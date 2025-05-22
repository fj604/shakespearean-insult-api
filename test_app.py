import pytest
from bs4 import BeautifulSoup # Added import
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_root_route(client):
    resp = client.get('/')
    assert resp.status_code == 200
    # Original check, can be kept or removed if specific header/footer checks are deemed sufficient.
    # For now, I'll keep it as it checks the <title> which is also important.
    assert b'Shakespearean Insults' in resp.data 

    soup = BeautifulSoup(resp.data, 'html.parser')

    # Test for header
    header = soup.find('header')
    assert header is not None, "Header element not found in HTML"
    
    h1 = header.find('h1')
    assert h1 is not None, "H1 element within header not found"
    # Using .strip() to avoid issues with potential leading/trailing whitespace
    assert h1.string.strip() == "Shakespearean Insult Generator", f"H1 text incorrect, got: '{h1.string.strip()}'"
    
    # Test for footer
    footer = soup.find('footer')
    assert footer is not None, "Footer element not found in HTML"
    
    p_in_footer = footer.find('p')
    assert p_in_footer is not None, "Paragraph element within footer not found"
    # Checking for presence of key text elements in the footer paragraph
    assert "©" in p_in_footer.text, "Copyright symbol '©' not found in footer paragraph"
    assert "GitHub" in p_in_footer.text, "Text 'GitHub' not found in footer paragraph"
    # Check for the link specifically
    footer_link = p_in_footer.find('a', href='#') # As per current HTML, href is '#'
    assert footer_link is not None, "Link to GitHub (href='#') not found in footer"
    assert "GitHub" in footer_link.text, "Text 'GitHub' not found in footer link"


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
