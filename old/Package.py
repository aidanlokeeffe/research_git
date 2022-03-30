class Package(list):
	def __init__(self, tag_list=None, hist_list=None):
		if tag_list == None or hist_list == None:
			tag_list = list()
			hist_list = list()
		self.append(tag_list)
		self.append(hist_list)

	def combine(self, other):
		self[0] += other[0]
		self[1] += other[1]

	def clear(self):
		self[0] = list()
		self[1] = list()

	def is_empty(self):
		return len(self[0]) == 0 and len(self[1]) == 0

	def has_collision(self):
		return len(self[0]) > 1

	def record(self, node):
		if len(self[0]) == 0:
			return
		for hist in self[1]:
			hist.append(node)

	def __str__(self):
		# Check is this is the empty package
		if self.is_empty():
			return "([],[])"

		st = "(["
		for tag in self[0]:
			st += str(tag) + ", "
		st = st[:-2] + "]; ["

		for hist in self[1]:
			st += str(hist) + ", "
		st = st[:-2] + "])"

		return st

	def __repr__(self):
		return str(self)