from flask import Flask, request, jsonify
import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

app = Flask(__name__)

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
    base_path = os.path.dirname(os.path.abspath(__file__))
    tokenizer_path = os.path.join(base_path, "../local_models", f"gpt2-lyrics-{artist}")
    return GPT2Tokenizer.from_pretrained(tokenizer_path)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    artist = data.get("artist", "")
    genre = data.get("genre", "")

    if not artist:
        return jsonify({"error": "Artist is required"})

    # Load model and tokenizer
    try:
        model = load_model(artist)
        tokenizer = load_tokenizer(artist)
    except Exception as e:
        return jsonify({"error": str(e)})

    # Default prompt for generation
    prompt = "This is a song about "

    print(f"Using prompt: {prompt}")

    # Generate lyrics
    try:
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        if inputs.size(1) == 0:
            return jsonify({"error": "Empty input tensor. The prompt may not be properly encoded."})
        attention_mask = torch.ones(inputs.shape, dtype=torch.long)
        outputs = model.generate(
            inputs,
            attention_mask=attention_mask,
            max_length=500,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            early_stopping=True,
            repetition_penalty=2.0,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Generated Text: {generated}")  # Debugging output
    except Exception as e:
        return jsonify({"error": str(e)})

    return jsonify({"lyrics": generated})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
