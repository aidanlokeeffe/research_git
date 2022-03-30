# This program writes simple scale free digraphs

###
# THERE BE BUGS IN THIS HERE CODE
###
import random
import numpy as np

# Returns the adjacency matrix
def get_sf_adj(n_final, in_exp, out_exp, out_name):
	# STEP 1: Calculate all the parameters
	c1 = 1 / (in_exp - 1)
	c2 = 1 / (out_exp - 1)

	# Sample valid a and b uniformly at random
	a = (1 - c1)*random.random() + c1
	while a == c1:
		a = (1 - c1)*random.random() + c1
	b = (1 - c2)*random.random() + c2
	while b == c2:
		b = (1 - c2)*random.random() + c2

	# Now we can calulate the parameters
	alpha = 1 - b
	beta = a + b - 1
	gamma = 1 - a
	delta_in = (alpha + beta - c1) / (alpha + gamma) / c1
	delta_out = (beta + gamma - c2) / (alpha + gamma) / c2

	# STEP 2: Initialize everything for the loop
	out = np.zeros((n_final, n_final))
	out[0,1] = 1
	t = 1
	if random.choice(range(2)):
		out[1,0] = 1
		t += 1

	nodes = [0, 1]
	n = 2

	in_dist = [0 for j in range(n_final)]
	out_dist = [0 for i in range(n_final)]

	# STEP 3: Construct the scale free digraph
	while True:
		# Update the in and out distributions
		for i in nodes:
			in_dist[i] = (np.sum(out[0:n,i]) + delta_in) / (t + delta_in*n)
			out_dist[i] = (np.sum(out[i,0:n]) + delta_out) / (t + delta_out*n)
		print(t)
		print(in_dist)
		print(out_dist)
		print()

		action = random.choices([0,1,2], weights=[alpha, beta, gamma], k=1)[0]

		if action==0:
			if n + 1 == n_final:
				break
			i = n
			j = random.choices(nodes, weights=in_dist[0:n], k=1)[0]
			out[i,j] += 1

			nodes.append(n)

			n += 1
		elif action==1:
			i = random.choices(nodes, weights=out_dist[0:n], k=1)[0]
			j = random.choices(nodes, weights=in_dist[0:n], k=1)[0]
			out[i,j] += 1
		else:
			if n + 1 == n_final:
				break
			
			j = n
			i = random.choices(nodes, weights=out_dist[0:n], k=1)[0]
			out[i,j] += 1

			nodes.append(n)

			n += 1
		
		# Update t
		t += 1

	# STEP 4: Write the digraph
	write_sf_graph(out, out_name)
	

# Writes the adjacency matrix to a file
def write_sf_graph(adj, out_name):
	out_file = open(out_name, "w")
	for i in range(adj.shape[0]):
		st = ""
		for j in range(adj.shape[1]):
			st += str(int(adj[i,j])) + ", "
		out_file.write(st[:-2] + "\n")
	out_file.close()

def main():
	get_sf_adj(15, 9, 10, "test_file.csv")




main()