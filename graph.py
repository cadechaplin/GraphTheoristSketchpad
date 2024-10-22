from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QPainterPath
from PyQt5.QtCore import Qt, QPoint
from node import Node
from edge import Edge
from events import Event
import math

class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.dragging_node = None
        self.selected = None
        self.DefaultPen = QPen(Qt.black, 2)
        self.SelectedPen = QPen(Qt.red, 2)
        self.SelectionChanged = Event()

    def add_node(self, name, pos):
        node = Node(name, pos)
        self.nodes.append(node)
        self.update()

    def add_edge(self, from_node, to_node, directional=False):
        edge = Edge(from_node, to_node)
        edge.directional = directional
        from_node.edges.append(edge)
        to_node.edges.append(edge)
        self.edges.append(edge)
        self.update()

    def paintEvent(self, event):
        edgeCounter = {}
        painter = QPainter(self)
        painter.setPen(self.DefaultPen)

        # Draw edges
        for edge in self.edges:
            #make sure pair is always in the same order
            if(edge.from_node.pos.x() < edge.to_node.pos.x()):
                pair = (edge.from_node, edge.to_node)
            else:
                pair = (edge.to_node, edge.from_node)
            
            count = edgeCounter.get(pair, 1)
            if edge == self.selected:
                painter.setPen(self.SelectedPen)
                self.draw_curved_edge(painter, edge.from_node.pos, edge.to_node.pos, edgeCounter.get(pair, 0), edge)
                #painter.drawLine(edge.from_node.pos , edge.to_node.pos )  # Adjust for the node size
                painter.setPen(self.DefaultPen)
            else:
                self.draw_curved_edge(painter, edge.from_node.pos, edge.to_node.pos, edgeCounter.get(pair, 0), edge)
                #painter.drawLine(edge.from_node.pos, edge.to_node.pos )  # Adjust for the node size
            edgeCounter[pair] = count + 1
        # Draw nodes
        for node in self.nodes:
            if node == self.selected:
                painter.setPen(Qt.red)  # Selected node color
            else:
                painter.setPen(self.DefaultPen)  # Default node color
            painter.setBrush(node.fill_color)
            painter.drawEllipse(int(node.pos.x() - (node.size / 2)), int(node.pos.y() - (node.size / 2)), int(node.size), int(node.size))  # Center the node drawing
            painter.drawText(int(node.pos.x() - (node.size / 2)), int(node.pos.y() - (node.size / 2)), node.name)  # Center the text
        painter.setPen(self.DefaultPen)
        
    def draw_curved_edge(self, painter, start, end, count, edge ):
        
        
        # If this is the first edge, draw it straight
        if count == 0:
            painter.drawLine(start, end)  # Draw a straight line for the first edge
            if edge.directional:
                # add triangle thing here
                None
            return
        # Curve is a scalar for offset, where offset is determined by the number of edges between the same nodes so far
        curve = 25
        offset = int((count)  // 2)
        # Create a QPainterPath for the curve
        path = QPainterPath()
        # Move to the starting point for the curve
        path.moveTo(start)

        # Calculate a control point to create a curve
        
        if count % 2 == 0:
            control_point = QPoint((start.x() + end.x()) // 2, (start.y() + end.y()) // 2 - (curve * offset))
        else:
            control_point = QPoint((start.x() + end.x()) // 2, (start.y() + end.y()) // 2 + (curve * offset))

        # Draw a cubic bezier curve
        path.cubicTo(control_point, control_point, end)

        # Draw the path
        painter.drawPath(path)
        
    def is_click_near_edge(self, click_pos, edge):
        from_pos = edge.from_node.pos
        to_pos = edge.to_node.pos

        # Calculate the distance from click_pos to the line segment (from_pos, to_pos)
        distance = self.point_to_line_distance(from_pos, to_pos, click_pos)

        # Define a threshold for the maximum distance from the edge to be considered "selected"
        threshold = 3  # Adjust this value as needed
        return distance < threshold

    def point_to_line_distance(self, from_pos, to_pos, click_pos):
        # Convert QPoint to tuples for easier calculations
        x1, y1 = from_pos.x(), from_pos.y()
        x2, y2 = to_pos.x(), to_pos.y()
        x0, y0 = click_pos.x(), click_pos.y()

        # Calculate the distance from point to line segment
        numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        denominator = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        if denominator == 0:
            return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)  # from_pos and to_pos are the same point
        return numerator / denominator
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            for node in self.nodes:
                # Check if the click is near the node
                distance_squared = ((node.pos.x() - event.pos().x()) ** 2 + (node.pos.y() - event.pos().y()) ** 2) ** (1/2)

                if distance_squared < int(node.size / 2):
                    self.dragging_node = node
                    self.update()  # Update to paint the selected node
                    break  # Stop checking after finding the first node

    def mouseMoveEvent(self, event):
        if self.dragging_node:
            new_pos = event.pos()
            # Ensure the node stays within the bounds of the screen
            new_pos.setX(max(int(self.dragging_node.size /2), min(new_pos.x(), self.width()-int(self.dragging_node.size /2))))
            new_pos.setY(max(int(self.dragging_node.size / 2), min(new_pos.y(), self.height() - int(self.dragging_node.size / 2))))
            self.dragging_node.pos = new_pos
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging_node = None
            
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selected = None
            
            for node in self.nodes:
                distance_squared = ((node.pos.x() - event.pos().x()) ** 2 + (node.pos.y() - event.pos().y()) ** 2) ** (1/2)
                if distance_squared < int(node.size / 2):
                    # Perform action on double-click
                    self.selected = node
                    print(f"Node {node.name} was double-clicked")
                    self.SelectionChanged.trigger()
                    self.update()
                    return
        
            for edge in self.edges:
                if self.is_click_near_edge(event.pos(), edge):
                    self.selected = edge
                    print(f"Edge from {edge.from_node.name} to {edge.to_node.name} was double-clicked")
                    self.SelectionChanged.trigger()
                    self.update()
                    return
            self.SelectionChanged.trigger()
            self.update()
            
