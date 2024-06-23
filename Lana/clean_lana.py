import os
import pandas as pd
import re

def clean_lyrics(lyrics):
    lyrics = re.sub(r'\[.*?\]', '', lyrics)  # Remove content inside brackets
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)  # Remove anything in parentheses or brackets
    lyrics = re.sub(r'[^\w\s]', '', lyrics)  # Remove punctuation
    lyrics = re.sub(r'\d+', '', lyrics)  # Remove numbers
    lyrics = re.sub(r'\s{2,}', ' ', lyrics)  # Replace multiple spaces with a single space
    lyrics = lyrics.lower()  # Convert to lowercase
    lyrics = lyrics.strip()  # Strip leading and trailing whitespaces
    return lyrics

def remove_unwanted_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Remove the first two lines and lines containing 'embed'
    cleaned_lines = [line for i, line in enumerate(lines) if i >= 2]
    
    # Remove 'embed' from lines and surrounding quotes
    cleaned_lines = [line.replace('"', '') for line in cleaned_lines]
    
    cleaned_lyrics = ''.join(cleaned_lines)
    
    return cleaned_lyrics

def combine_files(input_dir, temp_output_file, final_output_file):
    combined_lyrics = []

    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_dir, filename)
            cleaned_lyrics = remove_unwanted_lines(file_path)
            cleaned_lyrics = clean_lyrics(cleaned_lyrics)
            combined_lyrics.append(cleaned_lyrics)

    combined_df = pd.DataFrame({'lyrics': combined_lyrics})
    combined_df.to_csv(temp_output_file, index=False, header=False, quoting=3, escapechar='\\')  # quoting=3 corresponds to csv.QUOTE_NONE

    # Remove escape characters and 'embed' from the temporary file
    with open(temp_output_file, 'r', encoding='utf-8') as temp_file:
        temp_content = temp_file.read()
    
    # Clean up 'embed' and escape characters
    cleaned_content = temp_content.replace('\\', '').replace('embed', '')
    
    with open(final_output_file, 'w', encoding='utf-8') as final_file:
        final_file.write(cleaned_content)

def main():
    raw_dir = 'lana/lanaraw/Lana Del Rey'
    temp_combined_file = 'lana/processedlanalyrics/Lana_Del_Rey_combined_temp.csv'
    final_combined_file = 'lana/processedlanalyrics/Lana_Del_Rey_combined.csv'
    
    os.makedirs('lana/processedlanalyrics', exist_ok=True)  # Ensure the output directory exists
    combine_files(raw_dir, temp_combined_file, final_combined_file)

if __name__ == "__main__":
    main()
