import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def generate_lyrics(prompt, model_path='model_output', max_length=150):
    tokenizer = GPT2Tokenizer.from_pretrained(model_path)
    model = GPT2LMHeadModel.from_pretrained(model_path)

    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2, early_stopping=True)

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text

if __name__ == "__main__":
    prompt = "Write a song like Lady Gaga about chocolate cake"
    lyrics = generate_lyrics(prompt)
    print(lyrics)
