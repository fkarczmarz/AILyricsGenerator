import os
import deepl
from dotenv import load_dotenv
from flask import render_template, request, jsonify, send_file, send_from_directory
from webapp import app
from webapp.lyrics_generator import generate_final_lyrics
from webapp.melody_generator import generate_melody, save_melody_to_midi
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

load_dotenv()
DEEPL_API_KEY = os.getenv('DEEPL')

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

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    data = request.json
    lyrics = data.get('lyrics', '')
    if not lyrics:
        return jsonify({'error': 'No lyrics provided'}), 400

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "Generated Lyrics:")
    text = p.beginText(100, 730)
    for line in lyrics.split('\n'):
        text.textLine(line)
    p.drawText(text)
    p.showPage()
    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='lyrics.pdf', mimetype='application/pdf')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    lyrics = data.get('lyrics', '')
    target_lang = data.get('target_lang', 'EN')
    if not lyrics:
        return jsonify({'error': 'No lyrics provided'}), 400

    translator = deepl.Translator(DEEPL_API_KEY)
    result = translator.translate_text(lyrics, target_lang=target_lang)
    return jsonify({'translated_lyrics': result.text})

@app.route('/download_both_pdf', methods=['POST'])
def download_both_pdf():
    data = request.json
    original_lyrics = data.get('original_lyrics', '')
    translated_lyrics = data.get('translated_lyrics', '')
    if not original_lyrics or not translated_lyrics:
        return jsonify({'error': 'Lyrics missing'}), 400

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Page 1: Original Lyrics
    p.drawString(100, 750, "Original Lyrics:")
    text = p.beginText(100, 730)
    for line in original_lyrics.split('\n'):
        text.textLine(line)
    p.drawText(text)
    p.showPage()

    # Page 2: Translated Lyrics
    p.drawString(100, 750, "Translated Lyrics:")
    text = p.beginText(100, 730)
    for line in translated_lyrics.split('\n'):
        text.textLine(line)
    p.drawText(text)
    p.showPage()

    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='lyrics_both_versions.pdf', mimetype='application/pdf')
