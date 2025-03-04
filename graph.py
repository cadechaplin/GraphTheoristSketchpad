

import math
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QPainter, QPen, QPainterPath
from events import Event
from node import Node
from edge import Edge

class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.dragging_node = None
        self.selected = None
        self.DefaultPen = QPen(Qt.black, 2)
        self.SelectedPen = QPen(Qt.red, 2)
        self.CustomPen = QPen(Qt.black, 2)
        self.SelectionChanged = Event()

    def add_node(self, name, pos):
        node = Node(name, pos)
        self.nodes.append(node)
        self.update()
    
    def deleteSelected(self):
        if self.selected:
            if isinstance(self.selected, Node):
                self.nodes.remove(self.selected)
                i = len(self.edges) - 1
                while i > 0:
                    if self.edges[i].from_node == self.selected or self.edges[i].to_node == self.selected:
                        self.edges.remove(self.edges[i])
                    i -= 1
            elif isinstance(self.selected, Edge):
                self.edges.remove(self.selected)
            self.selected = None
            
            self.update()
        


    def add_edge(self, from_node, to_node, name, directional=False):
        existing_edges = []
        missing_edges = []
        for existing_edge in self.edges:
            if (existing_edge.from_node == from_node and existing_edge.to_node == to_node) or (existing_edge.from_node == to_node and existing_edge.to_node == from_node):
                existing_edges.append(existing_edge.count)
        for i in range(1, len(existing_edges) + 1):
            if i not in existing_edges:
                missing_edges.append(i)
        if len(missing_edges) > 0:
            edge = Edge(from_node, to_node, missing_edges[0], name)
        else:
            edge = Edge(from_node, to_node, len(existing_edges) + 1, name)

        edge.directional = directional
        from_node.edges.append(edge)
        to_node.edges.append(edge)
        self.edges.append(edge)
        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.DefaultPen)

        # Draw edges
        for edge in self.edges:
            if edge.from_node == edge.to_node:
                # Draw loop if the edge is a loop
                pair = (edge.to_node, edge.from_node)
                count = edge.count
                if edge == self.selected:
                    painter.setPen(self.SelectedPen)
                    self.draw_loop(painter, edge.from_node.pos, edge.from_node.size, (1 + .1*count))
                    painter.setPen(self.DefaultPen)
                else:
                    if(edge.fill_color != QColor(0, 0, 0)):
                        self.CustomPen.setColor(edge.fill_color)
                        painter.setPen(self.CustomPen)
                        self.draw_loop(painter, edge.from_node.pos, edge.from_node.size,(1 + .1*count))
                        painter.setPen(self.DefaultPen)
                    else:
                        self.draw_loop(painter, edge.from_node.pos, edge.from_node.size,(1 + .1*count))
                
            else:
                #make sure pair is always in the same order
                if(edge.from_node.pos.x() < edge.to_node.pos.x()):
                    pair = (edge.from_node, edge.to_node)
                else:
                    pair = (edge.to_node, edge.from_node)
            count = edge.count
            if edge == self.selected:
                painter.setPen(self.SelectedPen)
                self.draw_curved_edge(painter, edge.from_node.pos, edge.to_node.pos, count, edge)
                #painter.drawLine(edge.from_node.pos , edge.to_node.pos )  # Adjust for the node size
                painter.setPen(self.DefaultPen)
            else:
                if(edge.fill_color != QColor(0, 0, 0)):
                    self.CustomPen.setColor(edge.fill_color)
                    painter.setPen(self.CustomPen)
                    self.draw_curved_edge(painter, edge.from_node.pos, edge.to_node.pos, count, edge)
                    painter.setPen(self.DefaultPen)
                else:
                    self.draw_curved_edge(painter, edge.from_node.pos, edge.to_node.pos, count, edge)
                    #painter.drawLine(edge.from_node.pos, edge.to_node.pos )  # Adjust for the node size
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
        
    def draw_loop(self, painter, pos, size, scalar = 1):
        loop_size = size * scalar  # Adjust the loop size as needed
        path = QPainterPath()
        path.addEllipse(pos.x(), pos.y(), loop_size, loop_size)
        painter.drawPath(path)

    def is_click_near_edge(self, click_pos, edge):
        if(edge.from_node == edge.to_node):
            return self.is_click_near_loop(click_pos, edge)
        from_pos = edge.from_node.pos
        to_pos = edge.to_node.pos

        if (edge.count == 1):
            # Calculate the distance from click_pos to the line segment (from_pos, to_pos)
            distance = self.point_to_line_distance(from_pos, to_pos, click_pos)
            print(distance) # Debugging
            # Define a threshold for the maximum distance from the edge to be considered "selected"
            threshold = 3  # Adjust this value as needed
            return distance < threshold
        else:
            # Calculate the distance from click_pos to the curve
            curve = 25
            offset = int((edge.count)  // 2)
            if edge.count % 2 == 0:
                control_point = QPoint((from_pos.x() + to_pos.x()) // 2, (from_pos.y() + to_pos.y()) // 2 - (curve * offset))
            else:
                control_point = QPoint((from_pos.x() + to_pos.x()) // 2, (from_pos.y() + to_pos.y()) // 2 + (curve * offset))
            distance = self.point_to_line_distance(from_pos, control_point, click_pos)
            distance2 = self.point_to_line_distance(control_point, to_pos, click_pos)
            
            print(distance, distance2)  # Debugging
            return distance < 3 or distance2 < 3

    def is_click_near_loop(self, click_pos, edge):
        from_pos = edge.from_node.pos
        size = edge.from_node.size
        loop_size = (size * (1 + .1 * edge.count))
        loop_pos = QPoint(int(from_pos.x() + loop_size/2), int(from_pos.y() + loop_size / 2))
        x_distance = abs(click_pos.x() - loop_pos.x())
        y_distance = abs(click_pos.y() - loop_pos.y())
        distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
        print(distance) # Debugging
        print(click_pos)
        return (distance < loop_size / 2 + 3) and (distance > loop_size / 2 - 3)

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
            self.update()
            
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
                    print(f"Edge {edge.count} from {edge.from_node.name} to {edge.to_node.name} was double-clicked")
                    self.SelectionChanged.trigger()
                    self.update()
                    return
            self.SelectionChanged.trigger()
            self.update()
            
            
