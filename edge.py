

class Edge:
    def __init__(self, from_node, to_node, name):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.directional = True