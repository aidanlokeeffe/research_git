import numpy as np
import random
from math import isnan as isnan
from copy import deepcopy as deepcopy

from Container import Container
from Package import Package

class Experiment(object):
	# SETUP METHODS
	# Constructor
	def __init__(self, in_file, load, t_final, propagation_type=0, injection_type=0):
		self.adj = self.read_adjmat(in_file)
		self.size = len(self.adj)
		
		self.load = load
		self.t_final = t_final
		
		self.executed = False
		self.next_tag = 0
		self.results = {}

		self.state = self.initial_state()
		self.update_results(0)

		self.propagation_type = propagation_type
		self.propagate = self.set_propagate(self.propagation_type)
		self.injection_type = injection_type
		self.inject_helper = self.set_inject_helper(self.injection_type)


	def read_adjmat(self, in_file):
		outmat = np.genfromtxt(in_file, delimiter = ",")
		if isnan(outmat[0][0]):
			outmat = outmat[1:,1:]
		return outmat


	def set_propagate(self, propagation_type):
		try:
			return [self.IS_propagate, self.RW_propagate][self.propagation_type]
		except IndexError:
			raise ValueError("propagation_type must be 0 or 1")
		except TypeError:
			raise ValueError("propagation_type must be 0 or 1")


	def set_inject_helper(self, injection_type):
		try:
			return [self.nodes_worp, self.nodes_repl, self.nodes_unif, self.nodes_avbl][self.injection_type]
		except IndexError:
			raise ValueError("injection_type must be 0, 1, 2, or 3")
		except TypeError:
			raise ValueError("injection_type must be 0, 1, 2, or 3")


	# Initial state chosen uniformly at random from all possible states
	def initial_state(self):
		out = Container(self.size)
		for j in range(self.size):
			inject = random.choice([False, True])
			if inject:
				out[j] = Package([self.next_tag], [[j]])
				self.next_tag += 1
		return out


	# This method populates the results dictionary in such a way that
	# once a tag is no longer extant, the first index records the time of 
	# death and the second records the final number of generations
	def update_results(self, t):
		extant_tags = set()
		for j in range(self.size):
			extant_tags |= set(self.state[j][0])

		for tag in extant_tags:
			try:
				self.results[tag][0] += 1
				self.results[tag][1] += 1
			except KeyError:
				self.results[tag] = [t, 1]


	# DEBUGGING METHODS
	def clear_state(self):
		self.state.clear_all()


	def test_state_1(self):
		self.state = Container(self.size)
		self.next_tag = 0
		for j in range(self.size):
			if j % 2:
				self.state[j] = Package([j//2], [[j]])
				self.next_tag += 1


	def test_state_2(self):
		self.state.test_fill()
		self.next_tag = self.size


	# DYNAMICAL METHODS
	def IS_propagate(self):
		buffer = self.state.get_buffer()
		self.state.clear_all()

		for j in range(self.size):
			for i in range(self.size):
				if self.adj[i][j] and not buffer[i].is_empty():
					tag = deepcopy(buffer[i][0])
					hist = list(deepcopy(buffer[i][1]))
					incoming = Package(tag, hist)
					self.state[j].combine(incoming)
		
		self.state.record_all()


	def RW_propagate(self):
		buffer = self.state.get_buffer()
		self.state.clear_all()

		for i in range(self.size):
			if buffer[i].is_empty():
				continue

			out_neighbors = [j for j in range(self.size) if self.adj[i][j]]
			try:
				j = random.choice(out_neighbors)
				tag = deepcopy(buffer[i][0])
				hist = list(deepcopy(buffer[i][1]))
				incoming = Package(tag, hist)
				self.state[j].combine(incoming)
			except IndexError:
				continue

		self.state.record_all()


	def inject(self):
		injection_nodes = self.inject_helper()
		for node in injection_nodes:
			incoming = Package([self.next_tag], [[node]])
			self.state[node].combine(incoming)
			self.next_tag += 1


	# worp means without replacement
	def nodes_worp(self):
		return random.sample(range(self.size), self.load)


	# repl means with replacement
	def nodes_repl(self):
		return random.choices(range(self.size), k=self.load)


	# Uniform distribution over injections worp from loads 0 to self.size
	def nodes_unif(self):
		return [j for j in range(self.size) if random.choice(range(2))]


	# Injects worp no more than self.load packages into available places
	def nodes_avbl(self):
		available_nodes = [j for j in range(self.size) if self.state[j].is_empty()]
		L = len(available_nodes)
		
		if L <= self.load:
			return available_nodes
		else:
			return random.sample(available_nodes, self.load)


	def collide(self):
		for j in range(self.size):
			if self.state[j].has_collision():
				self.state[j].clear()


	def execute(self):
		if not self.executed:
			for t in range(1, self.t_final + 1):
				self.propagate()
				self.inject()
				self.update_results(t)
				self.collide()
			self.executed = True


	#OUTPUT METHODS
	def get_state(self):
		return self.state


	def is_executed(self):
		return self.executed


	def get_settings(self):
		st = "Number of nodes: " + str(self.size) + "\n"
		st += "Load: " + str(self.load) + "\n"
		st += "Time horizon: " + str(self.t_final) + "\n"

		st += "Propagation scheme: "
		if self.propagation_type == 0:
			st += "Information spreading\n"
		else:
			st += "Random walk\n"

		st += "Injection type: "
		if self.injection_type == 0:
			st += "Without replacement"
		elif self.injection_type == 1:
			st += "With replacement"
		elif self.injection_type == 2:
			st += "Random load, without replacement"
		else:
			st += "Available nodes, without replacement"

		return "\n" + st + "Executed: " + str(self.executed)


	def get_results(self):
		if not self.is_executed:
			raise AssertionError("Experiment not executed.")
		return self.results


	def write_results(self, out_name):
		if not self.is_executed:
			raise AssertionError("Experiment not executed.")
		out_file = open(out_name, "w")
		out_file.write("Tag, Time of Extinction, Number of Generations\n")
		for tag in self.results.keys():
			out_file.write(str(tag) + ", " + str(self.results[tag][0]) + ", " + str(self.results[tag][1]) +"\n")
		out_file.close()
