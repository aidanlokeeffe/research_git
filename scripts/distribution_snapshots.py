from Trial import Trial
import numpy as np

def make_distribution(in_dict, t_cutoff):
	out_dict = {}
	total = 0

	# Populate the output
	for t in range(t_cutoff + 1):
		try:
			new_data = in_dict[t]
		except KeyError:
			new_data = []

		for gens in new_data:
			try:
				out_dict[gens] += 1
			except KeyError:
				out_dict[gens] = 1
			total += 1

	# Normalize the output
	for gens in out_dict.keys():
		out_dict[gens] /= total

	return out_dict

def write_distributions(distributions, out_name):
	# Find the maximum number of generations ever attained
	max_gens = 0
	for dsbn in distributions:
		for gens in dsbn.keys():
			max_gens = max(max_gens, gens)

	out_file = open(out_name, "w")

	# Write headers
	st = "num_gens,"
	for i in range(1, len(distributions) + 1):
		st += "dist_" + str(i) + ","
	out_file.write(st[:-1] + "\n")

	for gens in range(1, max_gens+1):
		st = str(gens) + ","
		for dsbn in distributions:
			try:
				st += str(dsbn[gens])
			except KeyError:
				st += "0"
			st += ","
		out_file.write(st[:-1] + "\n")
	out_file.close()

def distribution_matrix(distributions):
	num_dsbns = 0
	max_gens = 0
	for dsbn in distributions:
		num_dsbns += 1
		for gens in dsbn.keys():
			max_gens = max(max_gens, gens)

	out_mat = np.zeros((max_gens, num_dsbns))

	for i in range(max_gens):
		for j in range(num_dsbns):
			try:
				out_mat[i,j] = distributions[j][i+1]
			except KeyError:
				continue

	return out_mat

def variational_distances_pairs(dsbn_mat):
	num_gens = dsbn_mat.shape[0]
	n = dsbn_mat.shape[1]
	out_mat = np.zeros((n,n))

	for i in range(n):
		for j in range(i+1, n):
			for k in range(num_gens):
				out_mat[i,j] += abs(dsbn_mat[k,i] - dsbn_mat[k, j])
			out_mat[i,j] /= 2
			out_mat[j,i] = out_mat[i,j]

	return out_mat

def variational_distances_consecutive(dsbn_mat):
	num_gens = dsbn_mat.shape[0]
	n = dsbn_mat.shape[1]

	out = []
	for i in range(1,n):
		dist = 0
		for k in range(num_gens):
			dist += abs(dsbn_mat[k,i] - dsbn_mat[k,i-1])
		out.append(dist/2)

	return out





def main():
	test = Trial("adjmats/monkey1.csv", 1, 200000, 1, 0)
	#test = Trial("adjmats/testadjmat.csv", 2, 80000, 1, 0)
	test.execute()
	final_results = test.get_final_results()

	distributions = []
	for c in range(1, 41):
		t_cutoff = c*5000
		dsbn = make_distribution(final_results, t_cutoff)
		distributions.append(dsbn)

	#write_distributions(distributions, "mk1_IS_L005_20000.txt")
	
	
	dsbn_mat = distribution_matrix(distributions)
	distance_mat = variational_distances_pairs(dsbn_mat)
	
	distances = variational_distances_consecutive(dsbn_mat)
	print("Pair, Variational Distance")
	for i in range(1, len(distances)):
		print( str((i-1, i)) + ", " + str(distances[i]) )
	


main()