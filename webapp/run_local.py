from flask import Flask, request, jsonify, render_template
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

model_cache = {}

def load_model(artist):
    base_path = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_path, "../local_models", f"gpt2-lyrics-{artist}")
    if artist not in model_cache:
        if not os.path.exists(model_path):
            raise ValueError(f"Model for artist {artist} does not exist at path {model_path}")
        model_cache[artist] = GPT2LMHeadModel.from_pretrained(model_path)
        print(f"Loaded model for artist {artist} from {model_path}")
    return model_cache[artist]

def load_tokenizer(artist):
    model_path = os.path.join("../local_models", f"gpt2-lyrics-{artist}")
    return GPT2Tokenizer.from_pretrained(model_path)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    artist = data.get("artist", "")
    genre = data.get("genre", "")
    
    # Debugging logs
    print(f"Received request with Artist: {artist}, Genre: {genre}")
    
    if not artist:
        return jsonify({"error": "Artist is required"})
    
    # Load model and tokenizer
    try:
        print("Loading model and tokenizer...")
        model = load_model(artist)
        tokenizer = load_tokenizer(artist)
        print("Model and tokenizer loaded successfully")
    except Exception as e:
        print(f"Error loading model or tokenizer: {e}")
        return jsonify({"error": str(e)})
    
    # Generate lyrics
    try:
        print("Generating lyrics...")
        prompt = f"Generate a song in the style of {artist} and genre {genre}."
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        outputs = model.generate(
            inputs,
            max_length=200,  # Increase this value to get longer texts
            num_return_sequences=2,
            no_repeat_ngram_size=2,
            early_stopping=True,
            repetition_penalty=3.0,
            temperature=2.1,
            top_p=0.5,
            do_sample=True
        )
        generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Generated text: {generated}")
    except Exception as e:
        print(f"Error generating lyrics: {e}")
        return jsonify({"error": str(e)})
    
    return jsonify({"lyrics": generated})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
