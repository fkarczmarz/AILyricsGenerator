import openai
import random
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json

# Ustaw swój klucz API OpenAI
openai.api_key = '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'

# Wczytaj plik CSV z tematyką
themes_file_path = '/content/AILyricsGenerator/Lana/Lana/processedlanalyrics/Lana_Del_Rey_individual_themes.csv'
themes_df = pd.read_csv(themes_file_path)

# Wczytanie wytrenowanego modelu
model_path = '/content/AILyricsGenerator/models/lana_lyrics_model.h5'
tokenizer_path = '/content/AILyricsGenerator/models/lana_tokenizer.json'

model = load_model(model_path)

with open(tokenizer_path, 'r') as f:
    tokenizer_data = json.load(f)
tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenizer_data)

# Ręczne ustawienie max_sequence_length
max_sequence_length = 100  # Ustaw wartość na podstawie długości sekwencji używanych podczas trenowania modelu

def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def generate_lyrics_from_model(seed_text, next_words=50, temperature=1.0, top_p=0.9, top_k=50, line_break_every=10):
    generated = []
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_length-1, padding='pre')
        preds = model.predict(token_list, verbose=0)[0]

        # Penalizacja za powtórzenia
        penalized_preds = preds.copy()
        for token in token_list[0]:
            penalized_preds[token] *= 0.7

        # Sampling z penalizacją, top-p i top-k
        if temperature > 0:
            preds = np.asarray(penalized_preds).astype('float64')
            preds = np.log(preds) / temperature
            exp_preds = np.exp(preds)
            preds = exp_preds / np.sum(preds)

        sorted_indices = np.argsort(preds)[::-1]
        cumulative_probs = np.cumsum(np.sort(preds)[::-1])
        
        top_p_indices = sorted_indices[cumulative_probs <= top_p]
        top_k_indices = sorted_indices[:top_k]
        
        filtered_indices = np.unique(np.concatenate((top_p_indices, top_k_indices)))
        filtered_preds = preds[filtered_indices]
        filtered_preds /= np.sum(filtered_preds)
        
        chosen_index = np.random.choice(filtered_indices, p=filtered_preds)

        output_word = ''
        for word, index in tokenizer.word_index.items():
            if index == chosen_index:
                output_word = word
                break

        if (len(generated) + 1) % line_break_every == 0:
            seed_text += "\n" + output_word
            generated.append("\n" + output_word)
        else:
            seed_text += " " + output_word
            generated.append(output_word)

    # Losowe dodanie interpunkcji
    lyrics_with_punctuation = []
    for word in generated:
        if random.random() < 0.1:
            word += random.choice([",", ".", "!", "?"])
        lyrics_with_punctuation.append(word)

    return ' '.join(lyrics_with_punctuation)

def generate_song(prompt, max_length=300):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=max_length,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def create_song_structure(lyrics):
    lines = lyrics.split('\n')
    verses = []
    chorus = []
    bridge = []
    current_section = "verse"

    for line in lines:
        if line.strip() == "":
            continue
        if "chorus" in line.lower():
            current_section = "chorus"
            continue
        if "bridge" in line.lower():
            current_section = "bridge"
            continue

        if current_section == "verse":
            verses.append(line)
        elif current_section == "chorus":
            chorus.append(line)
        elif current_section == "bridge":
            bridge.append(line)

    return verses, chorus, bridge

# Przykładowe użycie
seed_text = "In the summer haze of July"
generated_base_text = generate_lyrics_from_model(seed_text, next_words=50, temperature=1.0, top_p=0.9, top_k=50, line_break_every=10)

# Wybierz losową tematykę
random_theme = themes_df['themes'].sample().values[0]

prompt = (f"Write a full song with the theme '{random_theme}'. "
          f"Here is a base text to inspire you:\n\n{generated_base_text}\n\n"
          "Make sure to include verses, chorus, and bridge, and make the lyrics creative and coherent. "
          "Avoid mentioning the theme directly, but let it influence the mood and content of the song. "
          "Include some vocalizations like 'ah ah ah ah', 'oh', and similar expressions to make it sound more like a real song. "
          "The song should be rhythmic and have a natural flow, with varied line lengths and dynamic structure. "
          "It's very important to include lines that are shorter and longer, and not all lines need to rhyme.")

generated_song = generate_song(prompt, max_length=300)
verses, chorus, bridge = create_song_structure(generated_song)

print("Wygenerowana piosenka:\n")
print(generated_song)
print(f"\nWybrany temat: {random_theme}")