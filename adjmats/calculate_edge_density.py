import numpy as np
from math import isnan as isnan

def read_adjmat(in_file):
	out_mat = np.genfromtxt(in_file, delimiter = ",")
	if isnan(out_mat[0,0]):
		out_mat = out_mat[1:,1:]
	return out_mat

def count_edges(in_mat):
	m = in_mat.shape[0]
	n = in_mat.shape[1]

	out = 0
	for i in range(m):
		for j in range(n):
			if in_mat[i,j]:
				out += 1

	return out

def connection_density(in_file):
	adj = read_adjmat(in_file)

	nodes = adj.shape[0]
	edges = count_edges(adj)

	return nodes / nodes / (nodes-1)




def main():
	mk1 = str(connection_density("adjmats/monkey1.csv"))
	mk2 = str(connection_density("adjmats/monkey2.csv"))
	ms = str(connection_density("adjmats/mouse.csv"))


	out_file = open("connection_densities2.txt", "w")
	out_file.write("Connection Densities\n")
	out_file.write("    Monkey 1: " + mk1 + "\n")
	out_file.write("    Monkey 2: " + mk2 + "\n")
	out_file.write("    Mouse: " + ms)
	out_file.close()


main()