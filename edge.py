

class Edge:

    def __init__(self, from_node, to_node, count, name = "!unnamed edge!"):
        self.name = name

        self.from_node = from_node
        self.to_node = to_node
        self.directional = True
        self.count = count