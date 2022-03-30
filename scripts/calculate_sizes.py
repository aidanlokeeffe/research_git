from Experiment import Experiment
import numpy as np

test1 = Experiment("adjmats/monkey1.csv", 18, 10, 1, 0)
test2 = Experiment("adjmats/monkey2.csv", 18, 10, 1, 0)
test3 = Experiment("adjmats/mouse.csv", 18, 10, 1, 0)

print(test1.adj.shape[0], test1.adj.shape[1])
print(test2.adj.shape[0], test2.adj.shape[1])
print(test3.adj.shape[0], test3.adj.shape[1])