import openai
import pandas as pd
import os

openai.api_key = 'key'

# Lista 50 najpopularniejszych tematów
themes_list = [
    "Love", "Nostalgia", "Freedom", "Rebellion", "Passion", "Materialism", "Escapism", "Personal Growth",
    "Mental Health", "Danger", "Temptation", "Youth", "Loneliness", "Self-Discovery", "Heartbreak", "Addiction",
    "Friendship", "Hope", "Empowerment", "Relationships", "Desire", "Jealousy", "Recklessness", "Struggle",
    "Loss", "Adventure", "Self-Worth", "Music", "Celebration", "Identity", "Self-Expression", "Fame", "Beauty",
    "Mystery", "Power", "Acceptance", "Redemption", "Faith", "Family", "Sacrifice", "Trust", "Insecurity", "Confusion",
    "Dangerous Behavior", "Regret", "Spontaneity", "Happiness", "Fantasy", "Luxury", "Independence"
]

def get_themes_for_song(song_lyrics):
    prompt = (f"The following are the lyrics of a song. Based on these lyrics, choose the most fitting themes from the list: "
              f"{', '.join(themes_list)}.\n\n"
              f"Song Lyrics:\n{song_lyrics}\n\n"
              "Selected Themes:")

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=["\n"]
    )

    themes = response.choices[0].text.strip()
    return themes

def process_songs(input_folder, output_csv):
    rows = []

    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                song_lyrics = file.read()

            themes = get_themes_for_song(song_lyrics)
            if not themes:  # If themes are empty, try again
                themes = get_themes_for_song(song_lyrics)
            rows.append({'file_name': filename, 'themes': themes})

    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False)

input_folder = 'cleanlana/'
output_csv = 'Lana/extended_themes.csv'

process_songs(input_folder, output_csv)
