from PyQt5.QtCore import QPointF
from events import Event
import math

class Edge:

    def __init__(self, from_node, to_node, count, name = "!unnamed edge!"):
        self.name = name

        self.from_node = from_node
        self.to_node = to_node
        self.directional = True
        self.__count = count
        self.onDelete = Event()
        self.onChange = Event()
        # Register with both nodes
        from_node.addEdge(self)
        to_node.addEdge(self)

    def __del__(self):
        self.from_node.removeEdge(self)
        self.to_node.removeEdge(self)

    def getCount(self):
        return self.__count
    
    def getControlPoint(self):
        if self.to_node == self.from_node:
            # Self-loop handling unchanged
            node_pos = self.from_node.getPos()
            angle = (2 * math.pi / 10) * self.__count
            offset_distance = 50 + 20 * self.__count
            return node_pos + QPointF(math.cos(angle) * offset_distance, 
                                    math.sin(angle) * offset_distance)
        
        # For parallel edges
        midpoint = self.from_node.getPos() + (self.to_node.getPos() - self.from_node.getPos()) / 2
        direction = self.to_node.getPos() - self.from_node.getPos()
        perpendicular = QPointF(-direction.y(), direction.x())
        
        # Normalize perpendicular vector
        length = (perpendicular.x()**2 + perpendicular.y()**2)**0.5
        if length != 0:
            perpendicular /= length
            
            # Alternate sides for even/odd count and increase offset with count
            side = 1 if self.__count % 2 == 0 else -1
            offset = (self.__count + 1) // 2  # Increment offset for each pair
            offset_distance = 30 * offset * side
            return midpoint + perpendicular * offset_distance
        
        return midpoint
    