import os
import pandas as pd
import re

def clean_lyrics(lyrics):
    lyrics = lyrics.replace('"', '')  # Usuwanie wszystkich cudzysłowów

    lyrics_lines = lyrics.split('\n')
    cleaned_lines = [line for line in lyrics_lines if not re.match(r'^\[.*\]$', line) and 'Embed' not in line and line.strip() != '']
    cleaned_lyrics = '\n'.join(cleaned_lines)
    return cleaned_lyrics

def load_lyrics_files(input_dir):
    data = {}
    for artist_dir in os.listdir(input_dir):
        artist_path = os.path.join(input_dir, artist_dir)
        if os.path.isdir(artist_path):
            artist_lyrics = []
            print(f"Processing artist: {artist_dir}")
            for song_file in os.listdir(artist_path):
                if song_file.endswith('.csv'):
                    song_path = os.path.join(artist_path, song_file)
                    try:
                        df = pd.read_csv(song_path, error_bad_lines=False, warn_bad_lines=True)
                        lyrics = df.apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1).str.cat(sep='\n')
                        cleaned_lyrics = clean_lyrics(lyrics)
                        if len(cleaned_lyrics.split()) > 1:  # Sprawdzanie, czy plik ma więcej niż jedną linię
                            artist_lyrics.append(cleaned_lyrics)
                            print(f"Loaded: {song_path}")
                        else:
                            print(f"Skipping {song_path} due to insufficient data")
                    except Exception as e:
                        print(f"Error loading {song_path}: {e}")
            if artist_lyrics:
                data[artist_dir] = artist_lyrics
                print(f"Collected {len(artist_lyrics)} songs for artist: {artist_dir}")
    return data

def save_artist_datasets(data, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for artist, lyrics in data.items():
        artist_path = os.path.join(output_dir, f"{artist}_lyrics.csv")
        df = pd.DataFrame(lyrics, columns=['lyrics'])
        df.to_csv(artist_path, index=False, encoding='utf-8')
        print(f"Saved dataset for {artist} to {artist_path}")

def main():
    input_dir = os.path.join("..", "data", "raw_lyrics")
    output_dir = os.path.join("..", "data", "processed_lyrics")
    data = load_lyrics_files(input_dir)
    save_artist_datasets(data, output_dir)

if __name__ == "__main__":
    main()
