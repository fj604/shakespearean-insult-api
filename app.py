import insult
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def return_insult():
    return insult.insult()

if __name__ == '__main__':
    app.run()