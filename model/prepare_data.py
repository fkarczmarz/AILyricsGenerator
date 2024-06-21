import os
import pandas as pd
import re

def clean_lyrics(lyrics):
    # Usuń linie z nawiasami kwadratowymi oraz inne sekcje jak 'Embed'
    lyrics_lines = lyrics.split('\n')
    cleaned_lines = [line for line in lyrics_lines if not re.match(r'^\[.*\]$', line) and 'Embed' not in line]
    cleaned_lyrics = '\n'.join(cleaned_lines)
    return cleaned_lyrics

def load_lyrics_files(input_dir):
    data = []
    for artist in os.listdir(input_dir):
        artist_dir = os.path.join(input_dir, artist)
        if os.path.isdir(artist_dir):
            for song_file in os.listdir(artist_dir):
                if song_file.endswith('.csv'):
                    song_path = os.path.join(artist_dir, song_file)
                    try:
                        df = pd.read_csv(song_path, header=None, names=['lyrics'], usecols=[0], error_bad_lines=False, warn_bad_lines=True)
                        if 'lyrics' in df.columns:
                            lyrics = df['lyrics'].str.cat(sep='\n')
                            cleaned_lyrics = clean_lyrics(lyrics)
                            data.append({'artist': artist, 'lyrics': cleaned_lyrics})
                            print(f"Loaded: {song_path}")
                        else:
                            print(f"Skipped (missing columns): {song_path}")
                    except Exception as e:
                        print(f"Error loading {song_path}: {e}")
    return data

def save_dataset(data, output_path):
    if data:
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Dataset saved to {output_path}")
    else:
        print("No data to save")

def main():
    input_dir = os.path.join("..", "data", "raw_lyrics")
    output_path = os.path.join("..", "data", "lyrics_dataset.csv")
    data = load_lyrics_files(input_dir)
    print(f"Processed {len(data)} songs")
    save_dataset(data, output_path)

if __name__ == "__main__":
    main()
