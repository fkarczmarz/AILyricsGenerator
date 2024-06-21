import os
import pandas as pd

def remove_first_line(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        if len(lines) > 1:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(lines[1:])
            print(f"Removed first line from: {file_path}")
        else:
            print(f"File {file_path} has only one line, skipping.")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def clean_lyrics_files(input_dir):
    for artist in os.listdir(input_dir):
        artist_dir = os.path.join(input_dir, artist)
        if os.path.isdir(artist_dir):
            for song_file in os.listdir(artist_dir):
                if song_file.endswith('.csv'):
                    song_path = os.path.join(artist_dir, song_file)
                    remove_first_line(song_path)

# Ścieżka do katalogu z tekstami do oczyszczenia
raw_lyrics_dir = os.path.join("..", "data", "raw_lyrics")

# Uruchomienie procesu czyszczenia
clean_lyrics_files(raw_lyrics_dir)
