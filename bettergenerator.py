import pickle
import random
import sys

def to_bitmask(i): x = [0.0] * 34; x[i] = 1.0; return tuple(x)

def normalize(bits):
	val = max(bits)
	for i in xrange(len(bits)):
		if bits[i] == val:
			bits[i] = 1
		else:
			bits[i] = 0
	return bits

with open(sys.argv[1]) as f:
	chord_net = pickle.load(f)

with open(sys.argv[2]) as f:
	melody_net = pickle.load(f)

last = [0.0] * 34
last[random.randint(0,33)] = 1.0
tune = []
for _ in xrange(int(sys.argv[3])):
	val = max(last)
	for i in xrange(len(last)):
		if val == last[i]:
			tune.append(i)
			print last[i], i
	print ", ".join(str(last[x]) if x != i else "***" + str(last[x]) + "***" for x in range(len(last)))
	last = chord_net.activate(last).tolist()
real_tune = []
for beat in tune:
	last = to_bitmask(beat)
	for _ in xrange(3):
		val = max(last)
		for i in xrange(len(last)):
			if val == last[i]:
				real_tune.append(i)
		last = normalize(melody_net.activate(last).tolist())
with open(sys.argv[4], "w") as f:
	f.write("\n".join(map(str, tune)))
