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

def main():
	sizes = [91, 184, 212]
	in_stubs = ["ensembles/ms_monkey1/adjmat_", "ensembles/ms_monkey2/adjmat_", "ensembles/ms_mouse/adjmat_"]

	out_stubs = ["ensemble_means_mk1_", "ensemble_means_mk2_", "ensemble_means_ms_"]
	props = ["IS", "RW"]

	for c in range(2,3):
		size = sizes[c]
		in_stub = in_stubs[c]

		out_stub = out_stubs[c]

		for p in range(0,1):
			out_name = out_stub + props[p] + "_0.csv"
			out_file = open(out_name, "a")


			for net in range(500, 666):
				in_file = in_stub + str(net) + ".csv"
				st = ""

				for l in range(11):
					if l == 0:
						L = 1
					else:
						L = floor(0.10 * l * size)

					T = cutoff_times(p,c,l)

					trial = Trial(in_file, L, T, p, 0)
					trial.execute()

					st += str(trial.get_mean()) + ", "

				out_file.write(st[:-2] + "\n")

			out_file.close()

main()