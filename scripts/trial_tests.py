from Trial import Trial

def main():
	test = Trial("adjmats/testadjmat.csv", 2, 20, 0, 0)
	test.execute()
	
	'''
	# Make sure __init__ works as expected
	print("The adjacency matrix")
	print(test.adj)
	print()
	print("State at time 0")
	print(test.state)
	print()
	print("Raw results at time 0")
	print(test.raw_results)
	print()

	# Test out IS_propagate
	test.IS_propagate()
	print("State after information spreading")
	print(test.state)
	print()

	# Test out RW_propagate and set propagate
	test = Trial("adjmats/testadjmat.csv", 2, 20, 1, 0)
	print("New initial state")
	print(test.state)
	test.propagate()
	print()
	print("State after random walk")
	print(test.state)
	print()

	# Test the injection methods
	print(test.nodes_worp())
	print(test.nodes_repl())
	print(test.nodes_unif())
	print(test.nodes_avbl())
	print()

	# Test the execute method
	test = Trial("adjmats/testadjmat.csv", 2, 20, 0, 0)
	test.execute()

	# Test the collide method
	test.collide()

	print("Raw Results")
	for tag in test.raw_results.keys():
		print(str(tag) + ": " + str(test.raw_results[tag]))
	print()
	'''

	print("Final Results")
	for t in test.final_results.keys():
		print(str(t) + ": " + str(test.final_results[t]))
	print()

	print("Distribution and Mean")
	dsbn = test.get_distribution()
	print(dsbn)
	print(test.get_mean())

	# Does the distribution sum to 1?
	total = 0
	for g in dsbn.keys():
		total += dsbn[g]
	print(total)



main()