import numpy as np
import random
from math import isnan as isnan

class Trial(object):
	# SETUP METHODS
	# Constructor
	def __init__(self, in_file, load, t_final, propagation_type=0, injection_type=0):
		self.adj = self.read_adjmat(in_file)
		self.size = len(self.adj)

		self.load = load
		self.t_final = t_final

		self.executed = False
		self.next_tag = 0
		self.raw_results = {}

		self.state = self.initial_state()
		self.record(0)

		self.propagate = self.set_propagate(propagation_type)
		self.inject_helper = self.set_inject_helper(injection_type)

		self.final_results = {}
		self.distribution = {}

	def read_adjmat(self, in_file):
		out_mat = np.genfromtxt(in_file, delimiter = ",")
		if isnan(out_mat[0, 0]):
			out_mat = out_mat[1:, 1:]
		return out_mat

	# Choose a state uniformly at random
	def initial_state(self):
		out_state = [[] for j in range(self.size)]
		for j in range(self.size):
			inject = random.choice(range(2))
			if inject:
				out_state[j] += [self.next_tag]
				self.next_tag += 1
		return out_state


	# PROPAGATION METHODS
	# A message goes down every outgoing edge
	def IS_propagate(self):
		buffer = [[] for j in range(self.size)]

		for j in range(self.size):
			for i in range(self.size):
				buffer[j] += int(self.adj[i,j]) * self.state[i]

		self.state = buffer

	# A message goes down one randomly chosen outgoing edge
	def RW_propagate(self):
		buffer = [[] for j in range(self.size)]

		for i in range(self.size):
			if len(self.state[i]) > 0:
				out_neighbors = [j for j in range(self.size) if self.adj[i,j]]
				try:
					j = random.choice(out_neighbors)
					buffer[j] += self.state[i]
				except IndexError:
					continue

		self.state = buffer

	def set_propagate(self, propagation_type):
		try:
			return [self.IS_propagate, self.RW_propagate][propagation_type]
		except IndexError:
			raise ValueError("propagation_type must be 0 or 1")
		except ValueError:
			raise ValueError("propagation_type must be 0 or 1")


	# INJECTION METHODS
	# Choose self.load injection nodes without replacement
	def nodes_worp(self):
		return random.sample(range(self.size), self.load)

	# Choose self.load injection nodes with replacement
	def nodes_repl(self):
		return random.choices(range(self.size), k=self.load)

	# Choose between 0 and self.size injection nodes without replacement
	def nodes_unif(self):
		return [j for j in range(self.size) if random.choice(range(2))]

	# Choose up to self.load injection nodes from unoccupied nodes
	def nodes_avbl(self):
		available_nodes = [j for j in range(self.size) if len(self.state[j])==0]
		L = len(available_nodes)

		if L <= self.load:
			return available_nodes
		else:
			return random.sample(available_nodes, self.load)

	def set_inject_helper(self, injection_type):
		try:
			return [self.nodes_worp, self.nodes_repl, self.nodes_unif, self.nodes_avbl][injection_type]
		except IndexError:
			raise ValueError("injection_type must be 0, 1, 2, or 3")
		except TypeError:
			raise ValueError("injection_type must be 0, 1, 2, or 3")

	def inject(self):
		injection_nodes = self.inject_helper()
		for node in injection_nodes:
			self.state[node].append(self.next_tag)
			self.next_tag += 1 


	# OTHER DYNAMICAL METHODS
	def record(self, t):
		# Get the tags that still exist
		extant_tags = set()
		for j in range(self.size):
			extant_tags |= set(self.state[j])

		# Record the current time and the number of generations for each tag
		for tag in extant_tags:
			try:
				self.raw_results[tag][0] += 1
				self.raw_results[tag][1] += 1
			except KeyError:
				self.raw_results[tag] = [t, 1]

	def collide(self):
		for j in range(self.size):
			if len(self.state[j]) > 1:
				self.state[j] = []

	def execute(self):
		if not self.executed:
			self.executed = True

			# Run the dynamical process
			for t in range(1, self.t_final+1):
				self.propagate()
				self.inject()
				self.record(t)
				self.collide()

			# Get the final results
			for tag in self.raw_results.keys():
				extinction_time = self.raw_results[tag][0]
				try:
					self.final_results[extinction_time].append(self.raw_results[tag][1])
				except KeyError:
					self.final_results[extinction_time] = [self.raw_results[tag][1]]

			# Get the distribution
			total = 0
			for t in self.final_results.keys():
				gens = self.final_results[t]
				for g in gens:
					try:
						self.distribution[g] += 1
					except KeyError:
						self.distribution[g] = 1
					total += 1

			for g in self.distribution.keys():
				self.distribution[g] /= total

	# OUTPUT METHODS
	def get_raw_results(self):
		return self.raw_results

	def get_final_results(self):
		return self.final_results

	def get_distribution(self):
		return self.distribution

	def get_mean(self):
		out = 0
		total = 0
		for g in self.distribution.keys():
			out += g * self.distribution[g]
			total += self.distribution[g]
		return out / total
