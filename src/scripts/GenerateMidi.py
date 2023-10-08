import cv2
import numpy as np
import os
import colorsys
import math
import random

from mingus.core import chords
from midiutil import MIDIFile

color_folder = 'color'
out_folder = 'midi'
current_filename = ''

hex_to_sound_file_map_og = {
    '#000000': 'CC01.wav', #la bemol mayor (Ab)
    '#808080': 'CC01.wav',
    '#673AB7': 'CC01.wav',
    '#6B8E23': 'CC01.wav',
    '#8B0000': 'CC01.wav',
    '#800000': 'OpenHat01.wav', #mi bemol mayor (Eb)
    '#A52A2A': 'OpenHat01.wav',
    '#FFC0CB': 'OpenHat01.wav',
    '#FF69B4': 'OpenHat01.wav',
    '#0000FF': 'OpenHat01.wav',
    '#800080': 'SEM Sync-A#2.wav', #si bemol mayor (Bb)
    '#FFFF00': 'SEM Sync-A#2.wav',
    '#FFAA00': 'SEM Sync-A#2.wav',
    '#FF7F50': 'SEM Sync-A#2.wav',
    '#ADD8E6': 'SEM Sync-A#2.wav',
    '#40E0D0': 'SEM Sync-A#2.wav',
    '#00FFFF': 'SEM Sync-A#2.wav',
    '#FF8C00': 'Kick01.wav', #fa mayor (F)
    '#FFA500': 'Kick01.wav',
    '#000080': 'Kick01.wav',
    '#BA55D3': 'Kick01.wav',
    '#FFD1DC': 'Kick01.wav',
    '#AEC6CF': 'Kick01.wav',
    '#B0E0E6': 'SEM Sync-C2.wav', #do mayor (C)
    '#FFFFFF': 'SEM Sync-C2.wav',
    '#98FB98': 'SEM Sync-G2.wav', #sol mayor (G)
    '#E6E6FA': 'SEM Sync-G2.wav',
    '#65000B': 'SEM Sync-G2.wav',
    '#FFDF00': 'SEM Sync-G2.wav',
    '#FFD700': 'SEM Sync-D2.wav', #re mayor (D)
    '#FF0000': 'SEM Sync-D2.wav',
    '#8B4513': 'SEM Sync-A1.wav', #la mayor (A)
    '#FFA54F': 'SEM Sync-A1.wav',
    '#87CEEB': 'SEM Sync-A1.wav',
    '#00FF00': 'SEM Sync-A1.wav',
    '#39FF14': 'SEM Sync-E2.wav', #mi mayor (E)
    '#FFAD33': 'SEM Sync-E2.wav',
    '#FFFD37': 'SEM Sync-E2.wav',
    '#FF1A1A': 'SEM Sync-E2.wav',
    '#4682B4': 'si mayor', #si mayor (B)
    '#6E42BD': 'si mayor',
    '#C0C0C0': 'si mayor',
    '#DC143C': 'si mayor',
    '#9B0000': 'si mayor',
    '#050505': 'si mayor',
    '#FFDB1A': 'SEM Sync-F#2.wav', #fa sostenido mayor (F#)
    '#89D1EC': 'SEM Sync-F#2.wav',
    '#A0FFA0': 'SEM Sync-F#2.wav',
    '#FFB533': 'SEM Sync-F#2.wav',
    '#5C30A3': 'SEM Sync-F#2.wav',
    '#BEBEBE': 'SEM Sync-F#2.wav',
    '#7A0000': 'SEM Sync-C#1.wav', #do sostenido mayor (C#)
    '#191970': 'SEM Sync-C#1.wav',
    '#9400D3': 'SEM Sync-C#1.wav',
    '#F0E68C': 'SEM Sync-C#1.wav',
    '#708090': 'SEM Sync-C#1.wav',
    '#FAEBD7': 'SEM Sync-C#1.wav',
    '#008080': 'SEM Sync-C#1.wav',
    '#CC5500': 'SEM Sync-C#1.wav',
    '#787878': 'la bemol menor', #la bemol menor (Ab)
    '#A23E3E': 'la bemol menor',
    '#00008B': 'la bemol menor',
    '#7042C1': 'la bemol menor',
    '#A9A9A9': 'la bemol menor',
    '#1A1A1A': 'SEM Sync-E2.wav', #mi bemol menor (Eb)
    '#8C1A1A': 'SEM Sync-E2.wav',
    '#00009C': 'SEM Sync-E2.wav',
    '#AEDDEA': 'SEM Sync-E2.wav',
    '#00FF33': 'SEM Sync-E2.wav',
    '#030303': 'SEM Sync-A#1.wav', #si bemol menor (Bb)
    '#7F0000': 'SEM Sync-A#1.wav',
    '#708160': 'SEM Sync-A#1.wav',
    '#00007A': 'SEM Sync-A#1.wav',
    '#D2691E': 'SEM Sync-A#1wav',
    '#8B008B': 'SEM Sync-A#1.wav',
    '#696969': 'SEM Sync-A#1.wav',
    '#111111': 'SEM Sync-F1.wav', #fa menor (Fm)
    '#6A6A6A': 'SEM Sync-F1.wav',
    '#778899': 'SEM Sync-F1.wav',
    '#36454F': 'SEM Sync-F1.wav',
    '#750000': 'SEM Sync-F1.wav',
    '#656565': 'SEM Sync-C1.wav', #do menor (Dom)
    '#1A1A8C': 'SEM Sync-C1.wav',
    '#FF3300': 'SEM Sync-C1.wav',
    '#D1BECF': 'SEM Sync-C1.wav',
    '#D8BFD8': 'SEM Sync-C1.wav',
    '#ADADAD': 'SEM Sync-G1.wav', #sol menor (Solm)
    '#FFDA00': 'SEM Sync-G1.wav',
    '#98817B': 'SEM Sync-G1.wav',
    '#FAF0E6': 'SEM Sync-G1.wav',
    '#9A1010': 'SEM Sync-G1.wav',
    '#4B8CB8': 'SEM Sync-G1.wav',
    '#006400': 'SEM Sync-G1.wav',
    '#00007F': 'SEM Sync-D1.wav', #re menor (Rem)
    '#820000': 'SEM Sync-D1.wav',
    '#FFD9E2': 'SEM Sync-A2.wav', #la menor (Lam)
    '#FF6347': 'SEM Sync-A2.wav',
    '#C8A2C8': 'SEM Sync-A2.wav',
    '#FFCCE5': 'SEM Sync-E1.wav', #mi menor (Mim)
    '#FF5733': 'SEM Sync-E1.wav',
    '#4B627A': 'SEM Sync-E1.wav',
    '#ABABAB': 'SEM Sync-B1.wav', #si menor (Bm)
    '#536878': 'SEM Sync-B1.wav',
    '#68855C': 'SEM Sync-B1.wav',
    '#6334A7': 'SEM Sync-B1.wav',
    '#FFF5E1': 'SEM Sync-B1.wav',
    '#A7A7A7': 'SEM Sync-F#1.wav', #fa sostenido menor (F#m)
    '#5F7D8E': 'SEM Sync-F#1.wav',
    '#040404': 'SEM Sync-F#1.wav',
    '#790000': 'SEM Sync-F#1.wav',
    '#006600': 'SEM Sync-F#1.wav',
    '#9C857D': 'SEM Sync-F#1.wav',
    '#4A86BF': 'SEM Sync-G#2.wav', #do sostenido menor (C#m)
    '#10109A': 'SEM Sync-G#2.wav',
    '#3B4B58': 'SEM Sync-G#2.wav',
    '#7042C4': 'SEM Sync-G#2.wav',
    '#CBCBCB': 'SEM Sync-G#2.wav',
    '#AFEEEE': 'SEM Sync-G#2.wav',
    '#EAEAEA': 'SEM Sync-G#2.wav',
    
}

hex_to_sound_file_map = {
    '#000000': 'Ab',
    '#808080': 'Ab',
    '#673AB7': 'Ab',
    '#6B8E23': 'Ab',
    '#8B0000': 'Ab',
    '#800000': 'Eb',
    '#A52A2A': 'Eb',
    '#FFC0CB': 'Eb',
    '#FF69B4': 'Eb',
    '#0000FF': 'Eb',
    '#800080': 'Bb',
    '#FFFF00': 'Bb',
    '#FFAA00': 'Bb',
    '#FF7F50': 'Bb',
    '#ADD8E6': 'Bb',
    '#40E0D0': 'Bb',
    '#00FFFF': 'Bb',
    '#FF8C00': 'F',
    '#FFA500': 'F',
    '#000080': 'F',
    '#BA55D3': 'F',
    '#FFD1DC': 'F',
    '#AEC6CF': 'F',
    '#B0E0E6': 'C',
    '#FFFFFF': 'C',
    '#98FB98': 'G',
    '#E6E6FA': 'G',
    '#65000B': 'G',
    '#FFDF00': 'G',
    '#FFD700': 'D',
    '#FF0000': 'D',
    '#8B4513': 'A',
    '#FFA54F': 'A',
    '#87CEEB': 'A',
    '#00FF00': 'A',
    '#39FF14': 'E',
    '#FFAD33': 'E',
    '#FFFD37': 'E',
    '#FF1A1A': 'E',
    '#4682B4': 'B',
    '#6E42BD': 'B',
    '#C0C0C0': 'B',
    '#DC143C': 'B',
    '#9B0000': 'B',
    '#050505': 'B',
    '#FFDB1A': 'F#',
    '#89D1EC': 'F#',
    '#A0FFA0': 'F#',
    '#FFB533': 'F#',
    '#5C30A3': 'F#',
    '#BEBEBE': 'F#',
    '#7A0000': 'C#',
    '#191970': 'C#',
    '#9400D3': 'C#',
    '#F0E68C': 'C#',
    '#708090': 'C#',
    '#FAEBD7': 'C#',
    '#008080': 'C#',
    '#CC5500': 'C#',
    '#787878': 'Abm',
    '#A23E3E': 'Abm',
    '#00008B': 'Abm',
    '#7042C1': 'Abm',
    '#A9A9A9': 'Abm',
    '#1A1A1A': 'Ebm',
    '#8C1A1A': 'Ebm',
    '#00009C': 'Ebm',
    '#AEDDEA': 'Ebm',
    '#00FF33': 'Ebm',
    '#030303': 'Bbm',
    '#7F0000': 'Bbm',
    '#708160': 'Bbm',
    '#00007A': 'Bbm',
    '#D2691E': 'Bbm',
    '#8B008B': 'Bbm',
    '#696969': 'Bbm',
    '#111111': 'Fm',
    '#6A6A6A': 'Fm',
    '#778899': 'Fm',
    '#36454F': 'Fm',
    '#750000': 'Fm',
    '#656565': 'Cm',
    '#1A1A8C': 'Cm',
    '#FF3300': 'Cm',
    '#D1BECF': 'Cm',
    '#D8BFD8': 'Cm',
    '#ADADAD': 'Gm',
    '#FFDA00': 'Gm',
    '#98817B': 'Gm',
    '#FAF0E6': 'Gm',
    '#9A1010': 'Gm',
    '#4B8CB8': 'Gm',
    '#006400': 'Gm',
    '#00007F': 'Dm',
    '#820000': 'Dm',
    '#FFD9E2': 'Am',
    '#FF6347': 'Am',
    '#C8A2C8': 'Am',
    '#FFCCE5': 'Em',
    '#FF5733': 'Em',
    '#4B627A': 'Em',
    '#ABABAB': 'Bm',
    '#536878': 'Bm',
    '#68855C': 'Bm',
    '#6334A7': 'Bm',
    '#FFF5E1': 'Bm',
    '#A7A7A7': 'F#m',
    '#5F7D8E': 'F#m',
    '#040404': 'F#m',
    '#790000': 'F#m',
    '#006600': 'F#m',
    '#9C857D': 'F#m',
    '#4A86BF': 'C#m',
    '#10109A': 'C#m',
    '#3B4B58': 'C#m',
    '#7042C4': 'C#m',
    '#CBCBCB': 'C#m',
    '#AFEEEE': 'C#m',
    '#EAEAEA': 'C#m',   
}


NOTES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)

errors = {
    'notes': 'Bad input, please refer this spec-\n'
}

def swap_accidentals(note):
    if note == 'Db':
        return 'C#'
    if note == 'D#':
        return 'Eb'
    if note == 'E#':
        return 'F'
    if note == 'Gb':
        return 'F#'
    if note == 'G#':
        return 'Ab'
    if note == 'A#':
        return 'Bb'
    if note == 'B#':
        return 'C'

    return note

past_note = 'C'

def note_to_number(note: str, octave: int) -> int:
    global past_note
    note = swap_accidentals(note)
    if note not in NOTES:
        return past_note

    if octave not in OCTAVES:
        return past_note

    note = NOTES.index(note)
    note += (NOTES_IN_OCTAVE * octave)
    past_note = note

    assert 0 <= note <= 127, errors['notes']

    return note

def generate_midi2(current_midi, chord_progression):
    array_of_notes = chord_progression

    array_of_note_numbers = []
    octav = [3, 5 ,4]
    cont_octav = 0
    cont_notes = 0
    for note in array_of_notes:
        OCTAVE = octav[cont_octav]

        if(cont_notes == 2):
            cont_octav = (cont_octav+1)%3
            cont_notes = 0
        else:
            cont_notes += 1
        array_of_note_numbers.append(note_to_number(note, OCTAVE))

    track = 0
    channel = 0
    time = 0  # In beats
    duration = 1  # In beats
    tempo = 120  # In BPM
    volume = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
    # automatically)
    MyMIDI.addTempo(track, time, tempo)

    for i, pitch in enumerate(array_of_note_numbers):
        MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

    try: 
        os.mkdir(f'{out_folder}/{current_filename[0:-4]}')
    except OSError as error: 
        print(error)
    
    with open(f'{out_folder}/{current_filename[0:-4]}/{current_midi}.mid', "wb") as output_file:
        MyMIDI.writeFile(output_file)

def generate_midi(current_midi, chord_progression):
    array_of_notes = []
    for chord in chord_progression:
        array_of_notes.extend(chords.from_shorthand(chord)[0])

    array_of_note_numbers = []
    octav = [5, 5 ,5]
    cont_octav = 0
    cont_notes = 0
    for note in array_of_notes:
        OCTAVE = octav[cont_octav]

        if(cont_notes == 2):
            cont_octav = (cont_octav+1)%3
            cont_notes = 0
        else:
            cont_notes += 1
        array_of_note_numbers.append(note_to_number(note, OCTAVE))

    track = 0
    channel = 0
    time = 0  # In beats
    duration = 1  # In beats
    tempo = 120  # In BPM
    volume = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
    # automatically)
    MyMIDI.addTempo(track, time, tempo)

    for i, pitch in enumerate(array_of_note_numbers):
        MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

    try: 
        os.mkdir(f'{out_folder}/{current_filename[0:-4]}')
    except OSError as error: 
        print(error)
    
    with open(f'{out_folder}/{current_filename[0:-4]}/{current_midi}.mid', "wb") as output_file:
        MyMIDI.writeFile(output_file)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2 ,4))

def rgb_to_hsv(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h, s, v

def match_color_chord(color):
    h1, s1, v1 = rgb_to_hsv(hex_to_rgb(color))
    min_dist = float('inf')

    for color in hex_to_sound_file_map:
        h2, s2, v2 = rgb_to_hsv(hex_to_rgb(color))
        dist = math.sqrt((h2 - h1)**2 + (s2 - s1)**2 + (v2 - v1)**2)
        if dist < min_dist:
            min_dist = dist
            closest_color = color
    
    return hex_to_sound_file_map[closest_color]

def process(filename):
    current_midi = "0"
    current_chord_progression = []
    print()
    print(f'{filename}:')
    with open(filename, 'r') as file:
        for line in file:

            if(line[0] != current_midi):
                generate_midi(current_midi, current_chord_progression)
                print()
                print(f'{current_filename}/{current_midi}:')
                print(current_chord_progression)
                current_midi = line[0]
                current_chord_progression = []
            
            color = line[2:]
            chord = match_color_chord(color)
            current_chord_progression.append(chord)

    generate_midi(current_midi, current_chord_progression)
    print()
    print(f'{current_filename}/{current_midi}:')
    print(current_chord_progression)
    current_midi = line[0]
    current_chord_progression = []
            
def pipeline(filename):
    process(filename)

def main():
    global current_filename  # Declare current_filename as global
    for filename in os.listdir(color_folder):
        current_filename = filename
        pipeline(f'{color_folder}/{filename}')

if __name__ == "__main__":
    main()