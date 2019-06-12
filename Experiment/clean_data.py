'''
clean_data.py

This Python file takes in a log file from training AlphaZero and
converts to CSV a dataframe containing the loss and entropy of the
first batch of every trained game, plus the final winning rate when
playing against a MCTS player. The CSV is then used to visualize using R.
'''

import sys
import pandas as pd 

file = sys.argv[1]
f = open(file)

loss = []
entropy = []
ratio = []
playouts = []

for line in f:
	# find loss and entropy values
	if "batch: 0" in line:
		lists = line.split(",")
		for l in lists:
			if "loss:" in l:
				loss.append(float(l.replace("loss:", "")))
			elif "entropy:" in l:
				entropy.append(float(l.replace("entropy:", "")))
	# find winning ratio values 
	elif "Winning ratio" in line:
		ratio.append(float(line.split()[len(line.split()) - 1]))
	# find number of playouts
	elif "num_playouts" in line:
		v = line.split(":")[3].split(",")[0]
		playouts.append(float(v))

print(len(loss))
print(len(entropy))
print(len(ratio))
df = pd.DataFrame({"loss": loss, "entropy": entropy})
print(ratio)
print(playouts)

df.to_csv(file + ".csv")