import lyricsgenius
import os
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

client_access_token = '4nIv9c40XiYJl4ewGXFi-Boe-L-7HdnoroKf5NO8_fbjDv1s7bX9AiHm2u0LbTCW'
genius = lyricsgenius.Genius(client_access_token, remove_section_headers=True, skip_non_songs=True, timeout=80)

def clean_lyrics(lyrics):
    lyrics_lines = lyrics.split('\n')
    cleaned_lines = [line for line in lyrics_lines if not re.match(r'^\s*$', line) and not re.match(r'^\[.*\]$', line)]
    cleaned_lyrics = '\n'.join(cleaned_lines)
    return cleaned_lyrics

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_and_save_lyrics(artist_name, nb_songs=100):
    try:
        artist_genius = genius.search_artist(artist_name, max_songs=nb_songs, sort='popularity')
        if artist_genius is None:
            print(f"Nie udało się znaleźć artysty: {artist_name}")
            return
        
        songs = artist_genius.songs
        if len(songs) == 0:
            print(f"Nie znaleziono piosenek dla artysty: {artist_name}")
            return

        for song in songs:
            if song is not None:
                artist_dir = os.path.join("Lana", "lanaraw", artist_name)
                os.makedirs(artist_dir, exist_ok=True)
                
                cleaned_lyrics = clean_lyrics(song.lyrics)
                sanitized_title = sanitize_filename(song.title)
                song_data = pd.DataFrame({'artist': [artist_name], 'title': [sanitized_title], 'lyrics': [cleaned_lyrics]})
                song_filename = os.path.join(artist_dir, f"{sanitized_title}.csv")
                song_data.to_csv(song_filename, index=False, encoding="utf-8")
                print(f"Pobrano i zapisano tekst piosenki: {song.title}")

    except Exception as e:
        print(f"Error processing {artist_name}: {str(e)}")

def main():
    artist_name = "Lana Del Rey"
    download_and_save_lyrics(artist_name)

if __name__ == "__main__":
    main()
