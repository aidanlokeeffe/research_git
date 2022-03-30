import numpy as np
from math import isnan

def calculate_interval(mean, sd):
	z = 1.959964
	return (mean - z*sd, mean + z*sd)

def read_estimates(*in_files):
	m = 11
	n = len(in_files)

	out_mat = np.zeros((m,2*n))

	for i in range(n):
		data = np.genfromtxt(in_files[i], delimiter = ",")
		out_mat[0:m, 2*i] = data[1:m+1, -2]
		out_mat[0:m, 2*i+1] = data[1:m+1, -1]

	return out_mat

	

def main():
	z = 1.959964

	files = ["multiple_trials/multiple_trials_mk1_IS.txt",
	"multiple_trials/multiple_trials_mk1_RW.txt",
	"multiple_trials/multiple_trials_mk2_IS.txt",
	"multiple_trials/multiple_trials_mk2_RW.txt",
	"multiple_trials/multiple_trials_ms_IS.txt",
	"multiple_trials/multiple_trials_ms_RW.txt"]

	results = read_estimates(*files)

	# Get all the intervals 
	interval_mtx = np.zeros((results.shape[0], results.shape[1]))

	for i in range(results.shape[1]):
		if i%2 == 0:
			interval_mtx[:,i] = results[:,i] - z*results[:,i+1]
		else:
			interval_mtx[:,i] = results[:,i-1] + z*results[:,i]

	#for i in range(interval_mtx.shape[0]):
	#	print(list(interval_mtx[i]))

	names = ["Monkey 1, IS", "Monkey 1, RW", "Monkey 2, IS", "Monkey 2, RW", "Mouse, IS", "Mouse, RW"]

	out_file = open("confidence_intervals.txt", "w")
	for i in range(6):
		out_file.write(names[i] + "\n")
		for l in range(11):
			st = "    " + "L = " + str(l) + ": "
			st += str(interval_mtx[l, 2*i]) + ", "
			st += str(interval_mtx[l, 2*i + 1]) + "\n"
			out_file.write(st)

	out_file.close()
main()