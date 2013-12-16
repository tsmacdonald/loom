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

network = buildNetwork(INPUTS, HIDDEN, OUTPUTS, hiddenclass=LSTMLayer, outclass=SigmoidLayer, recurrent=True)
ds = SequentialDataSet(INPUTS, OUTPUTS)

def to_bitmask(i): x = [0.0] * INPUTS; x[i] = 1.0; return tuple(x)

files = glob.glob('l16_1d/*.csv')
tunes = []
for filename in files: #tune
	with open(filename) as f:
		notes = map(int, map(str.strip, f.readlines()))[::2]
		bitmasks = map(to_bitmask, notes)
		tunes.append(bitmasks)

for tune in tunes:
	ds.newSequence()
	for (inp, target) in zip(tune, tune[1:]):
		ds.appendLinked(inp, target)

network.randomize()

trainer = BackpropTrainer(network, ds, learningrate=.00001, momentum=.9)
import time
print "training..."
try:
  for _ in range(200):
    print "%d\t%f"%(_, trainer.train())
except KeyboardInterrupt:
	pass

import pickle
with open('network_newmomentum8_ds.pickled', 'w') as f:
	pickle.dump(network, f)
# from pybrain.tools.xml.networkwriter import NetworkWriter
# NetworkWriter.writeToFile(network, 'network1.xml')
		
