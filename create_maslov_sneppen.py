import numpy as np
import random
from math import isnan

def read_adjmat(in_file):
	out_mat = np.genfromtxt(in_file, delimiter = ",")
	if isnan(out_mat[0, 0]):
		out_mat = out_mat[1:, 1:]
	return out_mat

def randomize(in_mat, num_iter):
	m = in_mat.shape[0]
	n = in_mat.shape[1]
	out_mat = np.array([in_mat[i,j] for i in range(m) for j in range(n)] ).reshape((m,n))

	not_sinks = [i for i in range(m) if sum(in_mat[i,:]) > 0]

	for t in range(num_iter):
		abort_counter = 10000
		seeking = True

		while abort_counter and seeking:
			i = random.sample(not_sinks, 1)[0]
			valid_j = [j for j in range(n) if out_mat[i,j]]
			j = random.sample(valid_j, 1)[0]
			

			k = random.sample(not_sinks, 1)[0]
			valid_l = [l for l in range(n) if out_mat[k,l]]
			l = random.sample(valid_l, 1)[0]
			

			if out_mat[k,j] or out_mat[i,l]:
				abort_counter -= 1
				continue

			out_mat[i,j] = 0
			out_mat[k,l] = 0
			out_mat[k,j] = 1
			out_mat[i,l] = 1
			seeking = False

		if abort_counter == 0:
			raise AssertionError("Aborted on iter " + str(t))

	return out_mat


def write_adjmat(in_mat, out_name):
	m = in_mat.shape[0]
	n = in_mat.shape[1]

	out_file = open(out_name, "w")
	for i in range(m):
		st = ""
		for j in range(n):
			st += str(int(in_mat[i,j])) +", "
		out_file.write(st[:-2] + "\n")

	out_file.close()

def main():
	mk1 = read_adjmat("adjmats/monkey1.csv")
	mk2 = read_adjmat("adjmats/monkey2.csv")
	ms = read_adjmat("adjmats/mouse.csv")

	adjmats = [mk1, mk2, ms]
	
	num_iters = [161500, 527000, 1682100]
	
	names = ["ensembles/ms_monkey1/adjmat_",
	"ensembles/ms_monkey2/adjmat_",
	"ensembles/ms_mouse/adjmat_"]

	for idx in range(2,3):
		connectome = adjmats[idx]
		num_iter = num_iters[idx]
		name_stub = names[idx]
		for a in range(363, 400):
			adj = randomize(connectome, num_iter)
			out_name = name_stub + str(a) + ".csv"
			write_adjmat(adj, out_name)

		for a in range(866, 1000):
			adj = randomize(connectome, num_iter)
			out_name = name_stub + str(a) + ".csv"
			write_adjmat(adj, out_name)

main()