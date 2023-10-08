import csv
import sys
 
#from midiutil import MIDIFile
from mido import MidiFile, MidiTrack, Message


csv_file=sys.argv[1]
img_folder="imgs/"
csv_folder="color/"
def hex_to_hsv(hex_color):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:], 16) / 255.0  # Extract the entire hex color value
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    delta = max_val - min_val
    value = max_val
    if delta == 0:
        hue = 0
        saturation = 0
    else:
        if max_val == r:
            hue = 60 * (((g - b) / delta) % 6)
        elif max_val == g:
            hue = 60 * (((b - r) / delta) + 2)
        else:
            hue = 60 * (((r - g) / delta) + 4)
        saturation = delta / max_val
    return hue, saturation, value

midi_file = csv_file+".mid"
midi = MidiFile()
with open("color/"+csv_file, "r") as file:
    reader = csv.reader(file)
    track = MidiTrack()
    midi.tracks.append(track)

    for row in reader:
    
        hex_color = row[0].split()[1]  # Extract the hex color value correctly
        print(hex_color)
        hue, saturation, value = hex_to_hsv(hex_color)  # Add "#" to the hex value
        

        saturation= saturation*100
        value=value*100
        print(hue,saturation,value)
        if 0 < hue < 20 :
            note = 60
        elif 340 < hue < 10:
            note = 61
        elif 30 < hue < 45 :
            note = 62
        elif 45 < hue < 60 :
            note = 63
        elif 60 < hue < 90 :
            note = 64
        elif 90 < hue < 150:
            note = 65
        elif 140 < hue < 160:
            note = 66
        elif 160 < hue < 240:
            note = 67
        elif 190 < hue < 210:
            note = 68
        elif 270 < hue < 320:
            note = 69
        elif 240 < hue < 270:
            note = 70
        elif 320 < hue < 340:
            note = 71
        else:
            note=60
        # Add more conditions for other color ranges and notes here
        print(note)
        # Define MIDI note parameters
        velocity = int(saturation/100 * 127)
        duration = 480  # In beats, you can adjust this as needed
        note_on = Message("note_on", note=note, velocity=velocity, time=0)
        note_off = Message("note_off", note=note, velocity=0, time=duration)

        track.append(note_on)
        track.append(note_off)

midi.save("midi/"+midi_file)
print(f"MIDI file saved as {midi_file}")
