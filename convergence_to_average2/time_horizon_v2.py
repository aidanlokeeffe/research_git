from Trial import Trial
import numpy as np
import math

def get_mean_up_to(in_dict, t_cutoff):
	vals = []

	for t in range(t_cutoff+1):
		try:
			vals += in_dict[t]
		except KeyError:
			pass

	if len(vals) == 0:
		return 0
	return np.mean(vals)

def write_results(in_dict, out_name):
	out_file = open(out_name, "w")


	# The keys should be sorted due to the construction of the results dict
	# but they do need to be in order or else the Octave plots will look wrong
	for t in in_dict.keys():
		st = str(t) + ","
		for val in in_dict[t]:
			st += str(val) + ","
		out_file.write(st[:-1] + "\n")

	out_file.close()



def main():
	connectomes = ["adjmats/monkey1.csv", "adjmats/monkey2.csv", "adjmats/mouse.csv"]
	sizes = [91, 184, 212]

	names = ["mk1", "mk2", "ms"]
	prop_types = ["IS", "RW"]


	T = 100000
	step = 1000

	for idx in range(3):
		connectome = connectomes[idx]
		size = sizes[idx]
		name = names[idx]


		for prop in range(2):
			prop_type = prop_types[prop]

			results_dict = {t: [0,0,0,0,0,0,0,0,0,0,0] for t in range(0, T + step, step)}

			# Do an experiment for each load
			for l in range(11):
				# Compute the load parameter
				if l == 0:
					L = 1
				else:
					L = math.floor(0.10 * l * size)

				trial = Trial(connectome, L, T, prop, 0)
				trial.execute()
				results = trial.get_final_results()

				for t in range(0, T + step, step):
					val = get_mean_up_to(results, t)
					results_dict[t][l] = val

			# Assemble out_name
			out_name = "convergence_to_average_" + name + "_" + prop_type + ".txt"
			
			# Record the results dict to a file
			write_results(results_dict, out_name)



			



main()