import numpy as np
from math import isnan

def read_adjmat(in_file):
	out_mat = np.genfromtxt(in_file, delimiter=",")
	if isnan(out_mat[0,0]):
		out_mat = out_mat[1:,1:]
	return out_mat

def count_edges(adj):
	out = 0
	m = adj.shape[0]
	n = adj.shape[1]
	for i in range(m):
		for j in range(n):
			if adj[i,j]:
				out += 1
	return out

def connection_density(in_file):
	adj = read_adjmat(in_file)

	nodes = adj.shape[0]
	edges = count_edges(adj)

	return edges / nodes / (nodes - 1)

def main():
	out_file = open("connection_densities.txt", "w")

	out_file.write("Connection Densities\n")
	out_file.write("Monkey 1: " + str(connection_density("adjmats/monkey1.csv")) + "\n")
	out_file.write("Monkey 2: " + str(connection_density("adjmats/monkey2.csv")) + "\n")
	out_file.write("Mouse: " + str(connection_density("adjmats/mouse.csv")))

	out_file.close()

main()