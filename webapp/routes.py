from flask import render_template, request, jsonify, send_from_directory
from webapp import app
from webapp.lyrics_generator import generate_final_lyrics
from webapp.melody_generator import generate_melody, save_melody_to_midi

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_page')
def generate_page():
    return render_template('generate.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    result = generate_final_lyrics(data)
    return jsonify(result)

@app.route('/generate_melody', methods=['POST'])
def generate_melody_route():
    data = request.json
    lyrics = data.get('lyrics', '')
    if not lyrics:
        return jsonify({'error': 'No lyrics provided'}), 400

    melody = generate_melody(lyrics)
    melody_file = 'static/melody.mid'
    save_melody_to_midi(melody, melody_file)
    return jsonify({'melody_url': '/' + melody_file})

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)
