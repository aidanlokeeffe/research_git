from Trial import Trial
from math import floor
import numpy as np

def cutoff_times(p,c,l):
	exceptions = [[20000, 60000, 10000],
				  [40000, 40000, 30000]]
	normals = [2000, 1500, 1000, 1000, 500, 500, 500, 500, 500, 250]
	if l > 1:
		return normals[l-1]
	return exceptions[p][c]


def write_results(results_mat, out_name):
	m = results_mat.shape[0]
	n = results_mat.shape[1]

	out_file = open(out_name, "w")

	st = ""
	for j in range(n):
		st += "Ld" + str(j) + ", "
	out_file,write(st[:-2] + "\n")

	for i in range(m):
		st = ""
		for j in range(n):
			st += str(results_mat[i,j]) + ", "
		out_file.write(st[:-2] + "\n")

	out_file.close()

  propagation_type=0, injection_type=0

def main():
	sizes = [91, 184, 212]
	name_stubs = ["ensembles/ms_monkey1/adjmat_",
	"ensembles/ms_monkey2/adjmat_",
	"ensembles/ms_mouse/adjmat_"]

	out_stub = "ensemble_means_"
	name_caps = ["mk1_", "mk2_", "ms_"]
	props = ["IS", "RW"]




	for c in range(3):
		size = sizes[c]
		name_stub = name_stubs[c]

		for p in range(2):
			results_mat = np.zeros((1000, 11))
			out_name = out_stub + name_caps[c] + props[p] + ".csv"

			for net in range(1000):
				in_file = name_stub + str(net) + ".csv"
				for l in range(11):
					if l == 0:
						L = 1
					else:
						L = floor(0.10 * l * size)

					T = cutoff_times(p,c,l)

					trial = Trial(in_file, L, T, p, 0)
					trial.execute()
					results_mat[net, l] = trial.get_mean()

			write_results(results_mat, out_name)



main()