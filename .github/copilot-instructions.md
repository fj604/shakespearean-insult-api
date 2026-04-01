# Shakespearean Insult API

A Python Flask web application that generates random Shakespearean insults with both text and audio responses. The app serves a web interface where users can click Shakespeare's portrait to receive insults, and provides API endpoints for programmatic access.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

- Bootstrap and test the repository:
  - `cd /home/runner/work/shakespearean-insult-api/shakespearean-insult-api`
  - `python3 --version` (verify Python 3.12.3 is available)
  - `pip3 install -r requirements.txt` (takes ~15 seconds)
  - `python3 -m pytest test_app.py -v` (takes ~1 second, 3 passed/1 skipped)

- Test core functionality:
  - `python3 insult.py` (test insult generation directly)
  - `python3 app.py` (start development server on port 5000)
  - `curl http://127.0.0.1:5000/insult` (test API endpoint)

- Production deployment:
  - `gunicorn -w 2 --bind 127.0.0.1:8000 app:app` (production server)

- Docker deployment:
  - `docker build -t shakespearean-insult .` (may fail due to SSL cert issues in sandboxed environments)
  - Production deployment uses GitHub Actions with self-hosted runner

## Validation

- Always run the full test suite before making changes: `python3 -m pytest test_app.py -v`
- Test insult generation: `python3 insult.py` should output a Shakespearean insult
- Validate syntax: `find . -name "*.py" -exec python3 -m py_compile {} \;`
- Test web interface manually by starting Flask app and visiting http://127.0.0.1:5000
- For audio functionality testing, you need OPENAI_API_KEY environment variable set
- Always test both development (`python3 app.py`) and production (`gunicorn`) servers

## API Endpoints

- `GET /` - Serves the web interface (static/index.html)
- `GET /insult` - Returns a random Shakespearean insult as plain text
- `GET /audio` - Returns audio version of insult (requires OPENAI_API_KEY)

## Common Tasks

The following are outputs from frequently run commands. Reference them instead of viewing, searching, or running bash commands to save time.

### Repository Structure
```
.
├── .github/
│   ├── workflows/docker-image.yml
│   └── dependabot.yml
├── static/
│   ├── index.html
│   └── styles.css
├── app.py              # Main Flask application
├── insult.py           # Insult generation logic
├── test_app.py         # Test suite
├── requirements.txt    # Python dependencies
├── kit.txt            # Insult word combinations
├── Dockerfile         # Container configuration
├── README.md
└── STREAMING.md       # Audio streaming documentation
```

### Dependencies (requirements.txt)
```
Flask==3.1.1
Flask-Cors==6.0.1
gunicorn==23.0.0
openai
pytest
```

### Test Output
```bash
$ python3 -m pytest test_app.py -v
================================================= test session starts ==================================================
platform linux -- Python 3.12.3, pytest-8.4.1, pluggy-1.6.0 -- /usr/bin/python3
rootdir: /home/runner/work/shakespearean-insult-api/shakespearean-insult-api
plugins: anyio-4.10.0
collected 4 items                                                                                                      

test_app.py::test_root_route PASSED                                                                              [ 25%]
test_app.py::test_insult_route PASSED                                                                            [ 50%]
test_app.py::test_audio_route SKIPPED (Audio route requires OpenAI API access, which is not available in tes...) [ 75%]
test_app.py::test_cors_headers PASSED                                                                            [100%]

============================================= 3 passed, 1 skipped in 0.61s =============================================
```

### Sample Insult Output
```bash
$ python3 insult.py
Thou gleeking, crook-pated coxcomb!

$ curl http://127.0.0.1:5000/insult
Thou pribbling, shard-borne death-token!
```

## Project Structure

- **app.py**: Main Flask application with three routes:
  - `/` serves the web interface
  - `/insult` returns text insults 
  - `/audio` streams audio insults using OpenAI TTS
- **insult.py**: Core insult generation using random word combinations from kit.txt
- **test_app.py**: Comprehensive test suite with fixtures for testing routes and CORS
- **static/**: Web interface with clickable Shakespeare portrait and audio playback
- **kit.txt**: Contains ~600 lines of Shakespearean insult word combinations

## Environment Requirements

- **Python**: 3.12.3 (verified working)
- **Dependencies**: Install via `pip3 install -r requirements.txt`
- **Optional**: OPENAI_API_KEY environment variable for audio functionality
- **Ports**: Development server uses 5000, production uses 8000

## Known Issues

- Docker builds may fail in sandboxed environments due to SSL certificate verification issues
- Audio endpoint returns 500 error without OPENAI_API_KEY (this is expected behavior)
- External resources (Google Fonts, Wikipedia images) may be blocked in some environments but don't break core functionality
- No linting configuration files present (consider adding flake8 or black if code style consistency needed)

## CI/CD Pipeline

GitHub Actions workflow in `.github/workflows/docker-image.yml`:
- Triggers on pushes to `dev` and `main` branches
- Builds Docker image on self-hosted runner
- Deploys to production container on port 18000
- Requires OPENAI_API_KEY secret for audio functionality

## Development Workflow

1. Make code changes
2. Run syntax check: `find . -name "*.py" -exec python3 -m py_compile {} \;`
3. Run tests: `python3 -m pytest test_app.py -v`
4. Test locally: `python3 app.py` and verify endpoints work
5. Test production mode: `gunicorn -w 2 --bind 127.0.0.1:8000 app:app`
6. Commit changes (GitHub Actions will handle deployment)

## Audio Streaming Implementation

The `/audio` endpoint uses OpenAI's streaming TTS API to reduce latency. See STREAMING.md for technical details. Key points:
- Uses `openai.audio.speech.with_streaming_response.create()` for real-time streaming
- Returns chunked audio data with `Transfer-Encoding: chunked` header
- Includes insult text in `X-Insult-Text` response header
- Falls back gracefully when OpenAI API is unavailable