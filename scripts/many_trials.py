from Trial import Trial
import numpy as np
from math import floor

def write_output(results, out_name):
	out_file = open(out_name, "w")

	m = results.shape[0]
	n = results.shape[1]

	st = "Load, "
	for tau in range(n):
		st += "Trial" + str(tau+1) + ", "
	st += "Mean, StDev\n"
	out_file.write(st)

	for l in range(m):
		st = str(l) +", "
		for tau in range(n):
			st += str(results[l, tau]) + ", "

		st += str(np.mean(results[l,:])) + ", "
		st += str(np.std(results[l,:])) + "\n"

		out_file.write(st)

	out_file.close() 

def cutoff_times(p,c,l):
	exceptions = [[20000, 60000, 10000],
				  [40000, 40000, 30000]]
	normals = [2000, 1500, 1000, 1000, 500, 500, 500, 500, 500, 250]
	if l > 1:
		return normals[l-1]
	return exceptions[p][c]


def main():
	connectomes = ["adjmats/monkey1.csv", "adjmats/monkey2.csv", "adjmats/mouse.csv"]
	propagations = ["IS", "RW"]

	names = ["mk1", "mk2", "ms"]
	sizes = [91, 184, 212]

	for p in range(2):
		prop = propagations[p]
		for c in range(3):
			results = np.zeros((11, 10))
			connectome = connectomes[c]
			name = names[c]

			out_name = "multiple_trials_" + name + "_" + prop + ".txt"
			for l in range(11):
				if l == 0:
					L = 1
				else:
					L = floor(0.10*l*sizes[c])
				
				T = cutoff_times(p,c,l)

				for tau in range(10):
					trial = Trial(connectome, L, T, p, 0)
					trial.execute()
					val = trial.get_mean()

					results[l, tau] = val
			write_output(results, out_name)



main()