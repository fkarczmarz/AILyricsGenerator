import os
import pandas as pd

def clean_lyrics_file(file_path):
    try:
        df = pd.read_csv(file_path, error_bad_lines=False, warn_bad_lines=True)
        # Łączenie wszystkich kolumn w jedną kolumnę lyrics
        df['lyrics'] = df.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)
        df['lyrics'] = df['lyrics'].str.replace('"', '')  # Usunięcie wszystkich znaków cudzysłowu
        df['lyrics'] = df['lyrics'].str.replace(';', ',')  # Zamiana znaków ';' na ','
        df['lyrics'] = df['lyrics'].str.replace(',', ' ')  # Zamiana znaków ',' na ' ' (spację)
        df_cleaned = df[['lyrics']]  # Zachowujemy tylko kolumnę lyrics
        df_cleaned.to_csv(file_path, index=False, encoding='utf-8')
        print(f"Cleaned: {file_path}")
    except Exception as e:
        print(f"Error cleaning {file_path}: {e}")

def clean_processed_lyrics(input_dir):
    for artist_file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, artist_file)
        if file_path.endswith('.csv'):
            clean_lyrics_file(file_path)

def main():
    input_dir = os.path.join("..", "data", "processed_lyrics")
    clean_processed_lyrics(input_dir)

if __name__ == "__main__":
    main()
