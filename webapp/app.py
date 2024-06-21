from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json
import json

app = Flask(__name__)

# Ładowanie modelu i tokenizera
model = load_model('model/text_generator_model.h5')
with open('model/tokenizer.json', 'r') as file:
    tokenizer = tokenizer_from_json(json.load(file))

max_sequence_len = model.input_shape[1]

def generate_text(seed_text, next_words):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
        predicted = model.predict(token_list, verbose=0)
        predicted_word = tokenizer.index_word[np.argmax(predicted)]
        seed_text += " " + predicted_word
    return seed_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    seed_text = data['seed_text']
    next_words = int(data['next_words'])
    generated_text = generate_text(seed_text, next_words)
    return jsonify({'generated_text': generated_text})

if __name__ == '__main__':
    app.run(debug=True)
