from flask import Flask
from routes import generate

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Music Lyrics Generator!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
