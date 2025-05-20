import insult
from flask import Flask, send_file, Response
from flask_cors import CORS
import openai
import io

app = Flask(__name__)
CORS(app)

@app.route("/")
def serve_index():
    return send_file("index.html")

@app.route("/insult")
def return_insult():
    return insult.insult()

@app.route("/audio")
def insult_audio():
    text = insult.insult()
    response = openai.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="ballad",
        instructions="Imitate William Shakespeare swearing at a person",
        input=text,
        response_format="mp3",
    )
    audio_bytes = response.content
    resp = Response(audio_bytes, mimetype="audio/mpeg")
    resp.headers["X-Insult-Text"] = text
    return resp

if __name__ == '__main__':
    app.run()