import insult
from flask import Flask, send_file, Response
from flask_cors import CORS
import openai
import io

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
    response = openai.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="ballad",
        instructions="Imitate William Shakespeare insulting at a person",
        input=text,
        response_format="wav",
    )
    audio_bytes = response.content
    resp = Response(audio_bytes, mimetype="audio/wav")
    resp.headers["X-Insult-Text"] = text
    return resp

if __name__ == '__main__':
    app.run()