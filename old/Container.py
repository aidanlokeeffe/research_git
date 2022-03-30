from Package import Package

class Container(list):
    def __init__(self, size):
        self.size = size
        for _ in range(self.size):
            self.append(Package())

    def __str__(self):
        st = "{"
        for package in self:
            st += str(package) + ", "
        st = st[:-2] + "}"
        return st

    def __repr__(self):
        return str(self)


    def clear_all(self):
        for j in range(self.size):
            self[j].clear()

    def get_buffer(self):
        out = Container(self.size)
        out.combine(self)
        return out

    # Do I need this function?
    def record(self, j):
        self[j].record(j)

    def record_all(self):
        for j in range(self.size):
            self[j].record(j)

    def combine(self, other):
        for j in range(self.size):
            self[j].combine(other[j])

    def test_fill(self):
        for j in range(self.size):
            self[j] = Package([j], [[j, j+1]])