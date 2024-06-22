from transformers import GPT2Tokenizer, GPT2LMHeadModel
import os

def load_model(artist):
    model_path = os.path.join("/content/drive/MyDrive/models", f"gpt2-lyrics-{artist}")
    tokenizer = GPT2Tokenizer.from_pretrained(model_path)
    model = GPT2LMHeadModel.from_pretrained(model_path)
    return tokenizer, model

def generate_text(prompt, artist, genre):
    tokenizer, model = load_model(artist)
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text
