from flask import Blueprint, render_template, request
from .generate import generate_text

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    artist = request.form['artist']
    genre = request.form['genre']
    generated_text = generate_text(prompt, artist, genre)
    return render_template('index.html', generated_text=generated_text)
