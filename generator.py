import pickle
import random
import sys

def to_bitmask(i): x = [0.0] * 34; x[i] = 1.0; return tuple(x)

with open(sys.argv[1]) as f:
	net = pickle.load(f)
#net.reset()
last = [0.0] * 34
last[random.randint(0,33)] = 1.0
tune = []
for _ in xrange(int(sys.argv[2])):
#	if len(tune) >= 4 and tune[-1] == tune[-2] == tune[-3] == tune[-4]:# == tune[-5] == tune[-6] == tune[-7] == tune[-8]:
#		last[tune[-1]] = 0
	val = max(last)
	for i in xrange(len(last)):
		if val == last[i]:
			tune.append(i)
			print last[i], i
			#last[i] = max(0, min(1, last[i] - random.random() / 2))
			#last[i] += (1.0 - last[i]) / 2.0
			print last[i]
			#last = to_bitmask(i)
#		else:
#			last[i] = min(1, last[i] + random.random() / 4)
	print ", ".join(str(last[x]) if x != i else "***" + str(last[x]) + "***" for x in range(len(last)))
	#print last
	last = net.activate(last).tolist()
with open(sys.argv[3], "w") as f:
	f.write("\n".join(map(str, tune)))
