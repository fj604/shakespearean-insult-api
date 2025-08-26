import insult
from flask import Flask, send_file, Response
from flask_cors import CORS
import openai

# Configure Flask to serve static files from the 'static' directory at root URL
app = Flask(__name__, static_folder='static', static_url_path='/')
CORS(app)

# Explicitly serve index.html at the root URL
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route("/insult")
def return_insult():
    return insult.insult()

@app.route("/audio")
def insult_audio():
    text = insult.insult()
    print(f"Generating audio for insult: {text}")
    
    def generate_audio():
        try:
            with openai.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice="ballad",
                instructions="Imitate William Shakespeare insulting a person",
                input=text,
                response_format="wav",
            ) as response:
                for chunk in response.iter_bytes():
                    print(f"Received chunk of {len(chunk)} bytes")
                    yield chunk
        except Exception as e:
            # In case of API errors, we could fall back to an error message
            # For now, re-raise to let Flask handle it
            raise e
    
    resp = Response(generate_audio(), mimetype="audio/wav")
    resp.headers["X-Insult-Text"] = text
    resp.headers["Transfer-Encoding"] = "chunked"
    return resp

if __name__ == '__main__':
    app.run()