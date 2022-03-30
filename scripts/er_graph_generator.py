# This program writes loopless Erdos-Renyi graphs to the desired directory

import random

def er_graph(edge_prob, nodes, out_name):
	out_file = open(out_name, "w")

	for i in range(nodes):
		st = ""
		for j in range(nodes):
			if i == j:
				st += "0, "
			else:
				val = random.choices([0,1], weights=[1-edge_prob, edge_prob], k=1)[0]
				st += str(val) + ", "
		st = st[:-2]
		if i < nodes - 1:
			st += "\n"
		out_file.write(st)
	out_file.close()




def main():
	name_stubs = ["ensembles/er_monkey1/adjmat_",
	"ensembles/er_monkey2/adjmat_",
	"ensembles/er_mouse/adjmat_"]

	sizes = [91, 184, 212]

	probs = [0.1971916971916972, 0.15650985982418628, 0.37603952427792187]

	for i in range(3):
		name_stub = name_stubs[i]
		size = sizes[i]
		prob = probs[i]
		for j in range(10000):
			er_graph(prob, size, name_stub + str(j) + ".csv")


main()