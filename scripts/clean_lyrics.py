import os
import pandas as pd
import re

def clean_lyrics(lyrics):
    # Usuń wszystko przed pierwszym cudzysłowem i po ostatnim cudzysłowie
    match = re.search(r'"', lyrics)
    if match:
        lyrics = lyrics[match.start() + 1:]  # +1, żeby usunąć sam cudzysłów

    match = re.search(r'"[^"]*$', lyrics)  # szukaj ostatniego cudzysłowu
    if match:
        lyrics = lyrics[:match.start()]  # usuwanie ostatniego cudzysłowu i wszystkiego po nim

    # Usuń linie z nawiasami kwadratowymi oraz inne sekcje jak 'Embed'
    lyrics_lines = lyrics.split('\n')
    cleaned_lines = [line for line in lyrics_lines if not re.match(r'^\[.*\]$', line) and 'Embed' not in line]
    cleaned_lyrics = '\n'.join(cleaned_lines)
    return cleaned_lyrics

def clean_lyrics_files(input_dir):
    for artist in os.listdir(input_dir):
        artist_dir = os.path.join(input_dir, artist)
        if os.path.isdir(artist_dir):
            for song_file in os.listdir(artist_dir):
                if song_file.endswith('.csv'):
                    song_path = os.path.join(artist_dir, song_file)
                    with open(song_path, 'r', encoding='utf-8') as file:
                        lyrics = file.read()
                    
                    cleaned_lyrics = clean_lyrics(lyrics)
                    
                    with open(song_path, 'w', encoding='utf-8') as file:
                        file.write(cleaned_lyrics)
                    print(f"Cleaned: {song_path}")

# Ścieżka do katalogu z nieoczyszczonymi tekstami
raw_lyrics_dir = os.path.join("..", "data", "raw_lyrics")

# Uruchomienie procesu czyszczenia
clean_lyrics_files(raw_lyrics_dir)
