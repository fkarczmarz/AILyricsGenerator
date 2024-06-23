import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def generate_lyrics(artist, model_path='local_models', max_length=150):
    model_path = f"{model_path}/gpt2-lyrics-{artist}"
    tokenizer = GPT2Tokenizer.from_pretrained(model_path)
    model = GPT2LMHeadModel.from_pretrained(model_path)

    prompt = "This is a song"  # Default prompt
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(
        inputs,
        max_length=max_length,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        early_stopping=True,
        repetition_penalty=2.0
    )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text

if __name__ == "__main__":
    artist = "Lady Gaga"
    lyrics = generate_lyrics(artist)
    print(lyrics)
