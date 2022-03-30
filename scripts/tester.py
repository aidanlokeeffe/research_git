from Package import Package
from Container import Container
from Experiment import Experiment


'''
print("Package Tests")
a = Package([1], [[1,2,3]])
b = Package([2], [[4,5,6]])
print(a)
print(b)
a.combine(b)
print(a)
a.record(10)
print(a)
a.clear()
print(a)



print("\nContainer Tests")
A = Container(5)
A.test_fill()
print(A)
A.clear(4)
print(A)
A.record(3)
print(A)
B = Container(5)
B.test_fill()
A.combine(B)
print(A)
A.record_all()
print(A)
'''

print("\nExperiment Tests")
# IS, worp
trial = Experiment("adjmats/testadjmat.csv", 2, 10, propagation_type=0, injection_type=0)


#print("initial_state")
#print("Expected: {([], []), ([0], [[1]]), ([], []), ([1], [[3]]), ([], [])}")
#print("Actual: " + str(trial.get_state()) + "\n")

print("\nIS_propagate, test state 1")
trial.test_state_1()
trial.IS_propagate()
print("Expected: {([0], [[1, 0]]), ([], []), ([1], [[3, 2]]), ([0], [[1, 3]]), ([0], [[1, 4]])}")
print("Actual:   " + str(trial.get_state()))

print("\nRW_propagate, test state 2")
trial.test_state_2()
trial.RW_propagate()
print("Actual:   " + str(trial.get_state()))

print()
'''
print("\ninject_worp")
trial.clear_state()
for i in range(5):
	trial.inject_worp()
	print(trial.get_state())

print("\ninject_repl")
trial.clear_state()
for i in range(5):
	trial.inject_repl()
	print(trial.get_state())

print("\ninject_unif")
trial.clear_state()
for i in range(5):
	trial.inject_unif()
	print(trial.get_state())
	trial.clear_state()

print("\ninject_avbl")
trial.clear_state()
for i in range(10):
	trial.inject_avbl()
	print(trial.get_state())
'''
'''
trial = Experiment("adjmats/testadjmat.csv", 2, 10, propagation_type=0, injection_type=0)
trial.test_state_2()
print()
print(trial.get_state())
trial.propagate()
print()
print(trial.get_state())
trial.inject()
print()
print(trial.get_state())
trial.collide()
print()
print(trial.get_state())
'''
'''
for p in range(2):
	for i in range(4):
		trial = Experiment("adjmats/testadjmat.csv", 2, 6, p, i)
		trial.execute()
		results = trial.get_results()
		print("Propogation type " + str(p) + ", injection type " + str(i) + ":")
		print("    Key: [Time of Extinction, Number of Generations]")
		for key in results.keys():
			print("    " + str(key) + ": " + str(results[key]))
		if not (p==1 and i==3):
			print()
'''

#trial = Experiment("adjmats/testadjmat.csv", 2, 6, 0, 0)
#trial.execute()
##trial.write_results("test_results.m")
#final_results = trial.get_final_results()
#for key in final_results.keys():
#	print("    " + str(key) + ": " + str(final_results[key]))

