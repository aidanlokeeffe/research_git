from Experiment import Experiment
import numpy as np
import math

# Using the new trial class, this is now done during execution
def get_time_vs_gens(in_dict):
	out_dict = {}
	for tag in in_dict.keys():
		t = in_dict[tag][0]
		try:
			out_dict[t].append(in_dict[tag][1])
		except KeyError:
			out_dict[t] = [in_dict[tag][1]]

	T = max(out_dict.keys())

	return out_dict

# This method is obsolete. It's better to use the methods in Octave to plot the data
def write_plotter(in_dict, out_name, T_=None):
	# Determine the highest time
	if T_ == None:
		T = max(in_dict.keys()) + 1
	else:
		T = T_ + 1


	# Open the output file
	out_file = open(out_name, "w")

	# Write the t vector
	st = "t = ["
	for t in range(T):
		st += str(t) + ", "
	out_file.write(st[:-2] + "]\n")

	# Write the vector of averages
	st = "avg = ["
	data = []
	avg = 0
	for t in range(T):
		try:
			data += in_dict[t]
			avg = sum(data)/len(data)
		except KeyError:
			pass
		st += str(avg) + ", "
	out_file.write(st[:-2] + "]\n")

	out_file.write("figure\n"
		+ "plot(t, avg)\n"
		+ "title(\"Average Number of Generations at Time of Extinction\", \"FontSize\", 25)\n"
		+ "xlabel(\"t\", \"FontSize\", 16)\n"
		+ "ylabel(\"Average\", \"FontSize\", 16)")

	out_file.close()


["adjmats/cocoadj.csv"]

connectomes = ["adjmats/monkey1.csv", "adjmats/monkey2.csv", "adjmats/mouse.csv"]
sizes = [91, 184, 212]

T = 10000

for l in range(11):
	results_dict = {t: [0,0,0,0,0,0] for t in range(T+1)}
	col = 0
	for idx in range(3):
		for prop in range(2):
			# Compute the load parameter
			if l == 0:
				L = 1
			else:
				L = math.floor(0.10*l*sizes[idx])

			# Execute the experiment for the given parameters
			trial = Experiment(connectomes[idx], L, T, prop, 0)
			trial.execute()

			# Process the results
			result = trial.get_results()
			result = get_time_vs_gens(result)

			# Populate the results dictionary
			data = []
			for t in range(T+1):
				try:
					data += result[t]
					results_dict[t][col] = np.mean(data)
				except KeyError:
					if t == 0:
						continue
					results_dict[t][col] = results_dict[t-1][col]
			col += 1

	# Write the results to a text file
	out_file = open("convergence_to_average_" + str(l) + ".txt", "w")

	for t in range(T):
		st = str(t) + ","
		for idx in range(6):
			st += str(results_dict[t][idx]) + ","
		out_file.write(st[:-1] + "\n")
	out_file.close()






