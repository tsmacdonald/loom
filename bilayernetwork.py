#!/usr/bin/python
from pybrain.datasets import SequentialDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import SigmoidLayer
from pybrain.structure.modules.lstm import LSTMLayer

import glob

INPUTS = 34
HIDDEN = 15
OUTPUTS = 34

chord_network = buildNetwork(INPUTS, HIDDEN, OUTPUTS, hiddenclass=LSTMLayer, outclass=SigmoidLayer, recurrent=True)
melody_network = buildNetwork(INPUTS, HIDDEN, OUTPUTS, hiddenclass=LSTMLayer, outclass=SigmoidLayer, recurrent=True)
chord_ds = SequentialDataSet(INPUTS, OUTPUTS)
melody_ds = SequentialDataSet(INPUTS, OUTPUTS)

#def to_bitmask(i): x = [0.0] * INPUTS; x[i] = 1.0; return tuple(x)
def to_bitmask(i): return i

files = glob.glob('reel_nopickup/*.csv') #16th notes
tunes = []
for filename in files: #tune
	with open(filename) as f:
		notes = map(int, map(str.strip, f.readlines()))[::2] #8th ntoes
		bitmasks = map(to_bitmask, notes)
		tunes.append(bitmasks)

nested_tunes = map(lambda tune: [tune[x:min(len(tune) + 1, x+4)] for x in range(0, len(tune), 4)], tunes)


for tune in nested_tunes:
	for (inp, target) in zip(tune, tune[1:]):
		chord_ds.newSequence()
		chord_ds.appendLinked(inp[0], target[0])

for tune in tunes:
	for beat in tunes:
		for (inp, target) in zip(beat, beat[1:]):
			melody_ds.newSequence()
			melody_ds.appendLinked(inp, target)

chord_network.randomize()
melody_network.randomize()

chord_trainer = BackpropTrainer(chord_network, chord_ds, learningrate=.00001, momentum=.9)
melody_trainer = BackpropTrainer(melody_network, melody_ds, learningrate=.00001, momentum=.9)
import time
print "training chords..."
print "\n".join(map(str, chord_trainer.trainUntilConvergence()))
#try:
#  for _ in range(200):
#    print "%d\t%f"%(_, chord_trainer.train())
#except KeyboardInterrupt:
#	pass

print "training melody..."
print "\n".join(map(str, melody_trainer.trainUntilConvergence()))
#try:
#  for _ in range(200):
#    print "%d\t%f"%(_, melody_trainer.train())
#except KeyboardInterrupt:
#	pass

import pickle
with open('chord_network1.pickled', 'w') as f:
	pickle.dump(chord_network, f)
with open('melody_network1.pickled', 'w') as f:
	pickle.dump(melody_network, f)
# from pybrain.tools.xml.networkwriter import NetworkWriter
# NetworkWriter.writeToFile(network, 'network1.xml')
		
