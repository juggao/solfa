from midiutil import MIDIFile
import random, sys, argparse


bpm = 110
filename = ""
verbose = 0
output_file = "about.mid"
duration = 1.0
octave = 3

parser = argparse.ArgumentParser(
                    prog='solfamidi.py',
                    description='Generates a MIDI file from a "A - G#" string',
                    epilog='(c) 2023 René Oudeweg')

parser.add_argument('-f',  '--filename')           
parser.add_argument('-b', '--bpm')      
parser.add_argument('-v', '--verbose')
parser.add_argument('-o', '--output')
parser.add_argument('-d', '--duration')
parser.add_argument('-c', '--octave')


def translate_to_midi(text, output_file):
    # Set up MIDI parameters
    track = 0
    channel = 1
    time = 1  # In beats
    global duration
    global octave
    tempo = bpm  # In BPM
    volume = 100  # 0-127, as per MIDI standard

    # Create MIDIFile object with 1 track
    midi = MIDIFile(1)
    midi.addTempo(track, time, tempo)

    # Map notes to MIDI numbers octave = -1
    notes = {'A': 9, 'A#': 10, 'B': 1, 'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8}
    random.seed(5)
    
    # Convert text to MIDI notes
    for char in text.split(" "):
        if char in notes:
            note = notes[char]+(12*octave)
            random_volume = random.randint(68, 100)
            midi.addNote(track, channel, note, time, duration, random_volume)
            time += duration

    # Write MIDI data to file
    with open(output_file, 'wb') as file:
        midi.writeFile(file)





args = parser.parse_args()
#print(args.filename, args.bpm, args.verbose, args.output)
if args.bpm:
    bpm = int(args.bpm)
if args.octave:
    octave = int(args.octave)
if args.duration:
    duration = float(args.duration)
if not args.filename:
    filename = ""
else:
    filename = args.filename
if args.verbose:
    verbose = 1
if args.output:
    output_file = args.output
try:
    if verbose:
        print("opening: "+filename)
    with open(filename, 'r') as file:
        solfastring = file.read()
except FileNotFoundError:
    solfastring = sys.stdin.read()
    print("File not found.")
except IOError:
    print("Error reading the file.")
            

if verbose:
    print(solfastring)
translate_to_midi(solfastring, output_file)

