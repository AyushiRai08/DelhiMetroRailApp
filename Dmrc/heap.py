class Heap:
    def __init__(self):
        self.data = []
        self.map = {}

    def add(self, item):
        self.data.append(item)
        self.map[item] = len(self.data) - 1
        self.upheapify(len(self.data) - 1)

    def upheapify(self, ci):
        pi = (ci - 1) // 2
        if ci > 0 and self.is_larger(self.data[ci], self.data[pi]) > 0:
            self.swap(pi, ci)
            self.upheapify(pi)

    def swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]
        self.map[self.data[i]] = i
        self.map[self.data[j]] = j

    def display(self):
        print(self.data)

    def size(self):
        return len(self.data)

    def is_empty(self):
        return self.size() == 0

    def remove(self):
        self.swap(0, len(self.data) - 1)
        rv = self.data.pop()
        del self.map[rv]
        if not self.is_empty():
            self.downheapify(0)
        return rv

    def downheapify(self, pi):
        lci = 2 * pi + 1
        rci = 2 * pi + 2
        mini = pi

        if lci < len(self.data) and self.is_larger(self.data[lci], self.data[mini]) > 0:
            mini = lci

        if rci < len(self.data) and self.is_larger(self.data[rci], self.data[mini]) > 0:
            mini = rci

        if mini != pi:
            self.swap(mini, pi)
            self.downheapify(mini)

    def get(self):
        return self.data[0] if not self.is_empty() else None

    def is_larger(self, t, o):
        return (t > o) - (t < o)  # Returns 1 if t > o, -1 if t < o, 0 if equal

    def update_priority(self, item):
        if item in self.map:
            index = self.map[item]
            self.upheapify(index)
