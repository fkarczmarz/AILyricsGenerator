import pronouncing
import re
import note_seq
from note_seq.protobuf import music_pb2
from note_seq.protobuf.music_pb2 import NoteSequence
from note_seq import midi_io
import random

def get_stress(word):
    word = word.lower()
    phones = pronouncing.phones_for_word(word)
    if phones:
        stress_pattern = [int(s) for s in pronouncing.stresses(phones[0])]
        return stress_pattern
    else:
        # Handle contractions
        if "'" in word:
            parts = word.split("'")
            stress_pattern = []
            for part in parts:
                stress_pattern += get_stress(part)
            return stress_pattern
        # Handle hyphenated words
        elif '-' in word:
            parts = word.split('-')
            stress_pattern = []
            for part in parts:
                stress_pattern += get_stress(part)
            return stress_pattern
        else:
            print(f'Word not found in dictionary: {word}')
            # Skip the word if no stress pattern is found
            return []

def generate_melody(lyrics):
    stress_pattern = []
    words = re.findall(r'\b\w+\b', lyrics)

    # Get the stress pattern of the lyrics
    for word in words:
        stress_pattern.append(get_stress(word))

    # Flatten the stress_pattern list
    stress_pattern = [item for sublist in stress_pattern for item in sublist if isinstance(sublist, list)]

    print("Lyrics:", lyrics)
    print("Words:", words)
    print("Stress Patterns:", stress_pattern)

    # Generate a melody based on the stress pattern
    seq = NoteSequence()
    time = 0
    chord_prog = [60, 64, 67, 72]  # A simple Cmaj7 chord
    chord_index = 0
    pitch_offset = 0

    # Define sections and their properties
    sections = [
        {"name": "verse", "tempo": 120, "length": 16, "instrument": 0},
        {"name": "chorus", "tempo": 140, "length": 8, "instrument": 25},  # Acoustic Guitar
        {"name": "bridge", "tempo": 100, "length": 4, "instrument": 32},  # Acoustic Bass
    ]
    
    current_section = sections[0]
    section_index = 0
    section_time = 0

    # Define popular note sequences
    note_sequences = [
        [60, 62, 64, 65, 67, 69, 71, 72],  # Simple ascending scale
        [72, 71, 69, 67, 65, 64, 62, 60],  # Simple descending scale
        [60, 64, 67, 72, 67, 64, 60],  # Arpeggio
        [60, 62, 64, 67, 64, 62, 60],  # Ascending and descending
    ]
    note_sequence = random.choice(note_sequences)

    # Define popular chord progressions for guitar
    chord_progressions = [
        [60, 64, 67],  # C major
        [62, 65, 69],  # D minor
        [64, 67, 71],  # E minor
        [65, 69, 72],  # F major
        [67, 71, 74],  # G major
        [69, 72, 76],  # A minor
    ]

    for word, stress in zip(words, stress_pattern):
        word_length = len(word)
        if stress == 0:
            pitch = chord_prog[chord_index % len(chord_prog)] + pitch_offset
            duration = 0.25 * word_length
        elif stress == 1:
            pitch = chord_prog[(chord_index + 1) % len(chord_prog)] + pitch_offset
            duration = 0.5 * word_length
        elif stress == 2:
            pitch = chord_prog[(chord_index + 2) % len(chord_prog)] + pitch_offset
            duration = 0.75 * word_length
        elif stress == 3:
            pitch = chord_prog[(chord_index + 3) % len(chord_prog)] + pitch_offset
            duration = 1.0 * word_length

        # Ensure the note starts at a time aligned with the drum beat
        if time % 0.5 != 0:
            time = round(time / 0.5) * 0.5

        seq.notes.add(pitch=pitch, start_time=time, end_time=time+duration, velocity=80, instrument=current_section["instrument"])
        time += duration
        chord_index += 1
        pitch_offset = (pitch_offset + 1) % 12  # Change pitch to add variety
        section_time += duration

        # Change section if needed
        if section_time >= current_section["length"]:
            section_index = (section_index + 1) % len(sections)
            current_section = sections[section_index]
            section_time = 0

    # Add a bass line
    bass_pitch = 36  # C2
    bass_time = 0
    while bass_time < time:
        seq.notes.add(pitch=bass_pitch, start_time=bass_time, end_time=bass_time + 1.0, velocity=100, program=32, instrument=0)  # Acoustic Bass
        bass_time += 1.0

    # Add a drum line for rhythm on channel 10
    drum_time = 0
    while drum_time < time:
        seq.notes.add(pitch=36, start_time=drum_time, end_time=drum_time + 0.5, velocity=100, is_drum=True, program=0, instrument=9)  # Bass Drum
        drum_time += 0.5
        seq.notes.add(pitch=38, start_time=drum_time, end_time=drum_time + 0.25, velocity=100, is_drum=True, program=0, instrument=9)  # Snare Drum
        drum_time += 0.25
        seq.notes.add(pitch=42, start_time=drum_time, end_time=drum_time + 0.25, velocity=100, is_drum=True, program=0, instrument=9)  # Closed Hi-Hat
        drum_time += 0.25
        seq.notes.add(pitch=46, start_time=drum_time, end_time=drum_time + 0.25, velocity=100, is_drum=True, program=0, instrument=9)  # Open Hi-Hat
        drum_time += 0.25

    # Add harmony (e.g., a simple chord progression in the background)
    harmony_time = 0
    harmony_pitch = 60
    while harmony_time < time:
        for i, chord in enumerate(chord_prog):
            seq.notes.add(pitch=chord, start_time=harmony_time, end_time=harmony_time + 2.0, velocity=40, program=41, instrument=1)  # Violin
        harmony_time += 2.0
        harmony_pitch = (harmony_pitch + 1) % 12 + 60  # Slightly vary the pitch

    # Add continuous violin background for texture
    violin_pitch = 55  # G3
    violin_time = 0
    while violin_time < time:
        duration = random.uniform(4.0, 8.0)  # Long, continuous notes
        seq.notes.add(pitch=violin_pitch, start_time=violin_time, end_time=violin_time + duration, velocity=30, program=41, instrument=1)  # Violin
        violin_time += duration
        violin_pitch = (violin_pitch + 1) % 12 + 55  # Slightly vary the pitch

    # Add guitar chords for more texture
    guitar_time = 0
    while guitar_time < time:
        guitar_chords = random.choice(chord_progressions)
        for pitch in guitar_chords:
            duration = random.uniform(0.5, 1.5)
            seq.notes.add(pitch=pitch, start_time=guitar_time, end_time=guitar_time + duration, velocity=70, program=25, instrument=2)  # Acoustic Guitar
        guitar_time += 0.8

    seq.total_time = time
    seq.tempos.add(qpm=current_section["tempo"])

    return seq

def save_melody_to_midi(melody, filename):
    midi_io.sequence_proto_to_midi_file(melody, filename)
