# Chord of the day - Created by Alvaro Aguirre

import random
from chord_dictionary import chords

chromatic = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

def scale(root):
    """Returns the major scale of the root note"""
    root_pos = chromatic.index(root)
    reorder = chromatic[root_pos:len(chromatic)] + chromatic[0:root_pos]
    scale_pos = [0,2,4,5,7,9,11]
    major = [reorder[i] for i in scale_pos]
    return(major)
    
def sharp(note):
    """Returns the note sharp"""
    position = chromatic.index(note)
    if position == len(chromatic)-1:
        return(chromatic[0])
    else:
        return(chromatic[position+1])
    
def flat(note):
    """Returns the note flatted"""
    position = chromatic.index(note)
    if position == 0:
        return(chromatic[-1])
    else:
        return(chromatic[position-1])
    
    
def get_notes(root, positions):
    """Given a list of positions, returns the notes"""
    notes = []
    major = scale(root)
    if isinstance(positions,list) != True:
        positions = [positions]
    for pos in positions:
        if "b" in str(pos):
            pos = int(pos.replace("b",""))
            if (pos > 7):
                pos = pos % 7
            notes.append(flat(major[pos-1]))
        elif "#" in str(pos):
            pos = int(pos.replace("#",""))
            if (pos > 7):
                pos = pos % 7
            notes.append(sharp(major[pos-1]))
        else:
            if (pos > 7):
                pos = pos % 7
            notes.append(major[pos-1])
    return(notes)

def in_string(note, string_note):
    """Finds fret on a string"""
    # First reorder the chromatic scale so it starts on the string_note
    note_pos = chromatic.index(string_note)
    reorder = chromatic[note_pos:len(chromatic)] + chromatic[0:note_pos]
    # Now get the position of the note
    return(reorder.index(note))


def get_random_chord():
    root = random.choice(chromatic)
    chord = random.choice(list(chords.items()))
    name = root + " " + chord[0]
    notes = get_notes(root, chord[1])
    random_chord = {}
    random_chord["root"] = root
    random_chord["major_scale"] = scale(root)
    random_chord["name"] = name
    random_chord["notes"] = notes
    random_chord["positions"] = chord[1]
    return(random_chord)


chord_of_day = get_random_chord()

message = """\
Subject: Chord of the day""" + chord_of_day["name"] + """

Hi,

The chord of the day is """ + chord_of_day["name"] + """

The positions that construct this type of chord are: 
""" + str(chord_of_day["positions"]) + """

Its root note is """ + chord_of_day["root"] + """, which has the following major scale:
""" + str(chord_of_day["major_scale"]) + """

And the notes that compose """ + chord_of_day["name"] + """ are:
""" + str(chord_of_day["notes"]) + """

Go build it on the guitar! You can start on fret """ + str(in_string(chord_of_day["root"], "E")) + """ of the 6-th string, or fret """ + str(in_string(chord_of_day["root"], "A")) + """ of the 5-th string.

Enjoy,
Alvaro Aguirre
"""

print(message)