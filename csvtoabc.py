def int_to_note(num):
	num += 38
	pitch_index = num % 12
	pitch = ['C', 'C', 'D', 'E', 'E', 'F', 'F', 'G', 'G', 'A', 'B', 'B'][pitch_index]
	if pitch_index in [0, 2, 4, 5, 7, 9, 11]:
		accidental = ""
	elif pitch_index in [1, 6, 8]:
		accidental = "^"
	elif pitch_index in [3, 10]:
		accidental = "_"
	pitch = accidental + pitch
	octave = num / 12
	if octave <= 4:
		pitch += ',' * abs(4 - octave)
	else:
		pitch = pitch.lower() + "'" * (octave - 5)
	return pitch

if __name__ == '__main__':
	import sys
	with open(sys.argv[1]) as f:
		notes = []
		for line in f:
			notes.append(int_to_note(int(line)))
	print """
X:1
T:%s
L:1/16
K:C"""%sys.argv[1]
	measure = False
	for i in xrange(0, len(notes), 4):
		out = "".join([notes[i], notes[i + 1], notes[i + 2], notes[i + 3]])
		print out,
		if measure: print " | ",
		measure = not measure
	print " ",
	print "]"
