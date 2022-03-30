from Experiment import Experiment
import numpy as np

test1 = Experiment("adjmats/monkey1.csv", 18, 10, 1, 0)
test2 = Experiment("adjmats/monkey2.csv", 18, 10, 1, 0)
test3 = Experiment("adjmats/mouse.csv", 18, 10, 1, 0)

'''
test.execute()
results = test.get_results()
for key in results.keys():
	st = str(key) + ": " + str(results[key])
	print(st)
'''

for test in [test1, test2, test3]:
	N = len(test.adj)
	num_out_neighbors = np.sum(test.adj, 1)
	print( len([j for j in range(N) if num_out_neighbors[j]==0]) )
