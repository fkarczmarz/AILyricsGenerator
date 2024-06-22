from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import os

app = Flask(__name__)

model_cache = {}

def load_model(artist):
    model_path = os.path.join("/content/drive/MyDrive/models", f"gpt2-lyrics-{artist}")
    if artist not in model_cache:
        if not os.path.exists(model_path):
            raise ValueError(f"Model for artist {artist} does not exist at path {model_path}")
        model_cache[artist] = GPT2LMHeadModel.from_pretrained(model_path)
        print(f"Loaded model for artist {artist} from {model_path}")
    return model_cache[artist]

def load_tokenizer():
    return GPT2Tokenizer.from_pretrained("gpt2")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    artist = data.get("artist", "")
    genre = data.get("genre", "")
    
    # Debugging logs
    print(f"Prompt: {prompt}")
    print(f"Artist: {artist}")
    print(f"Genre: {genre}")
    
    if not artist:
        return jsonify({"error": "Artist is required"})
    
    # Load model and tokenizer
    try:
        model = load_model(artist)
        tokenizer = load_tokenizer()
    except Exception as e:
        return jsonify({"error": str(e)})
    
    # Generate lyrics
    try:
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        outputs = model.generate(inputs, max_length=500, num_return_sequences=1)
        generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Generated text: {generated}")
    except Exception as e:
        return jsonify({"error": str(e)})
    
    return jsonify({"lyrics": generated})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
