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
    def getCount(self):
        return self.__count
    
    def getControlPoint(self):
        if self.to_node == self.from_node:
            # Calculate the control point for self-loops
            node_pos = self.from_node.getPos()
            angle = (2 * math.pi / 10) * self.__count  # Adjust the divisor to control the spread of self-loops
            offset_distance = 50 + 20 * self.__count  # Adjust the base distance and multiplier as needed
            control_point = node_pos + QPointF(math.cos(angle) * offset_distance, math.sin(angle) * offset_distance)
            return control_point
        # Calculate the midpoint
        midpoint = self.from_node.getPos() + (self.to_node.getPos() - self.from_node.getPos()) / 2

        # Calculate the perpendicular vector
        direction = self.to_node.getPos() - self.from_node.getPos()
        perpendicular = QPointF(-direction.y(), direction.x())

        # Normalize the perpendicular vector
        length = (perpendicular.x()**2 + perpendicular.y()**2)**0.5
        if length != 0:
            perpendicular /= length

        # Offset the control point based on the count
        offset_distance = 20 * self.__count  # Adjust the multiplier as needed
        control_point = midpoint + perpendicular * offset_distance

        return control_point
    