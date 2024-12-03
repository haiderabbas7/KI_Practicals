class LifoQueue:

    def __init__(self):
        self.nodes = []

    def push(self, data):
        self.nodes.append(data)

    def pop(self):
        if not self.is_empty():
            return self.nodes.pop()

    def peek(self):
        if not self.is_empty():
            return self.nodes[len(self.nodes) - 1]

    def is_empty(self):
        return len(self.nodes) == 0

    def size(self):
        return len(self.nodes)


class FifoQueue:

    def __init__(self):
        self.nodes = []

    def enqueue(self, data):
        self.nodes.append(data)

    def dequeue(self):
        if not self.is_empty():
            return self.nodes.pop(0)

    def peek(self):
        if not self.is_empty():
            return self.nodes[0]

    def contains(self, data):
        return data in self.nodes

    def is_empty(self):
        return len(self.nodes) == 0

    def size(self):
        return len(self.nodes)


class PrioQueue:

    def __init__(self):
        self.nodes = []

    def __contains__(self, item):
        return any(node.equals(item) for _, node in self.nodes)

    def enqueue(self, data, prio):
        node = (prio, data)
        self.nodes.append(node)
        self.nodes.sort()

    def dequeue(self):
        if not self.is_empty():
            node = self.nodes.pop(0)
            return node[1]

    def peek(self):
        if not self.is_empty():
            node = self.nodes[0]
            return node[1]

    def is_empty(self):
        return len(self.nodes) == 0

    def size(self):
        return len(self.nodes)
