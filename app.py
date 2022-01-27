import insult
from flask import Flask

app = Flask(__name__)

@app.route("/")
def return_insult():
    return insult.insult()

if __name__ == '__main__':
    app.run()