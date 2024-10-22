import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget, QVBoxLayout, QPushButton, QInputDialog, QLabel, QLineEdit
from PyQt5.QtWidgets import QSlider, QColorDialog
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QPainterPath

class Event:
    def __init__(self):
        self.update = []
    def trigger(self):
        for func in self.update:
            func()
    
class Node:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.edges = []
        self.size = 40
        self.fill_color = Qt.lightGray
        

class Edge:
    def __init__(self, from_node, to_node):
        self.name = ""
        self.from_node = from_node
        self.to_node = to_node
        self.directional = False

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

    def add_edge(self, from_node, to_node):
        edge = Edge(from_node, to_node)
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
            if edge.from_node == edge.to_node:
                # Draw loop if the edge is a loop
                if edge == self.selected:
                    painter.setPen(self.SelectedPen)
                    self.draw_loop(painter, edge.from_node.pos, edge.from_node.size)
                    painter.setPen(self.DefaultPen)
                else:
                    self.draw_loop(painter, edge.from_node.pos, edge.from_node.size)
            else:
                #make sure pair is always in the same order
                if(edge.from_node.pos.x() < edge.to_node.pos.x()):
                    pair = (edge.from_node, edge.to_node)
                else:
                    pair = (edge.to_node, edge.from_node)
            
                count = edgeCounter.get(pair, 1)
                if edge == self.selected:
                    painter.setPen(self.SelectedPen)
                    self.draw_curved_edge(painter, edge.from_node.pos, edge.to_node.pos, edgeCounter.get(pair, 0))
                    #painter.drawLine(edge.from_node.pos , edge.to_node.pos )  # Adjust for the node size
                    painter.setPen(self.DefaultPen)
                else:
                    self.draw_curved_edge(painter, edge.from_node.pos, edge.to_node.pos, edgeCounter.get(pair, 0))
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
        
    def draw_curved_edge(self, painter, start, end, count):
        # If this is the first edge, draw it straight
        if count == 0:
            painter.drawLine(start, end)  # Draw a straight line for the first edge
            return
        curve = 25
        # Create a QPainterPath for the curve
        path = QPainterPath()
        # Move to the starting point for the curve
        path.moveTo(start)

        # Calculate a control point to create a curve
        if count % 2 == 0:
            control_point = QPoint((start.x() + end.x()) // 2, (start.y() + end.y()) // 2 - curve)
        else:
            control_point = QPoint((start.x() + end.x()) // 2, (start.y() + end.y()) // 2 + curve)

        # Draw a cubic bezier curve
        path.cubicTo(control_point, control_point, end)

        # Draw the path
        painter.drawPath(path)
        
    def draw_loop(self, painter, pos, size):
        loop_size = size * 1.2  # Adjust the loop size as needed
        path = QPainterPath()
        path.addEllipse(pos.x(), pos.y(), loop_size, loop_size)
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
            self.dragging_node.pos = event.pos()
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
            


class EditMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.graph = None
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create NodeMenu and EdgeMenu layouts
        self.NodeMenu = QVBoxLayout()
        self.EdgeMenu = QVBoxLayout()

        # Common controls
        self.name_label = QLabel("Name:")
        self.name_edit = QLineEdit()
        self.color_button = QPushButton("Choose Color")

        # Node-specific controls
        self.size_label = QLabel("Size:")
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setRange(10, 100)  # Adjust range as needed for node size

        # Add controls to NodeMenu
        self.NodeMenu.addWidget(self.name_label)
        self.NodeMenu.addWidget(self.name_edit)
        self.NodeMenu.addWidget(self.color_button)
        self.NodeMenu.addWidget(self.size_label)
        self.NodeMenu.addWidget(self.size_slider)

        # Add controls to EdgeMenu
        self.EdgeMenu.addWidget(self.name_label)
        self.EdgeMenu.addWidget(self.name_edit)
        self.EdgeMenu.addWidget(self.color_button)

        # Add NodeMenu and EdgeMenu to the main layout
        self.layout.addLayout(self.NodeMenu)
        self.layout.addLayout(self.EdgeMenu)

        # Initially hide all controls
        self.hide_node_controls()
        self.hide_edge_controls()

        # Variable to store the currently selected item (Node or Edge)
        self.selected_item = None

        # Connect signals
        self.color_button.clicked.connect(self.choose_color)
        self.name_edit.textChanged.connect(self.update_name)
        self.size_slider.valueChanged.connect(self.update_size)

    def choose_color(self):
        if self.selected_item:
            color = QColorDialog.getColor()
            if color.isValid():
                self.selected_item.fill_color = color  # Assume Node and Edge both have a 'color' attribute
                self.update_item()

    def update_name(self, text):
        if self.selected_item:
            self.selected_item.name = text
            self.update_item()

    def update_size(self, value):
        if self.selected_item and isinstance(self.selected_item, Node):
            self.selected_item.size = value
            self.update_item()

    def update_item(self):
        # Redraw the graph after any change
        self.graph.update()

    def updateSelection(self, item):
        self.selected_item = item
        if isinstance(item, Node):
            # Show Node controls
            self.show_node_controls()

            # Set values for Node editing
            self.name_edit.setText(item.name)
            self.size_slider.setValue(item.size)

        elif isinstance(item, Edge):
            # Show Edge controls
            self.show_edge_controls()

            # Set values for Edge editing
            self.name_edit.setText(item.name)

        else:
            # Hide all controls when no item is selected
            self.hide_node_controls()
            self.hide_edge_controls()

            self.selected_item = None

        self.update()

    def show_node_controls(self):
        # Show all Node controls
        self.name_label.show()
        self.name_edit.show()
        self.color_button.show()
        self.size_label.show()
        self.size_slider.show()

    def hide_node_controls(self):
        # Hide all Node controls
        self.name_label.hide()
        self.name_edit.hide()
        self.color_button.hide()
        self.size_label.hide()
        self.size_slider.hide()

    def show_edge_controls(self):
        # Show all Edge controls
        self.name_label.show()
        self.name_edit.show()
        self.color_button.show()
        self.size_label.hide()  # Edge does not need size control
        self.size_slider.hide()  # Edge does not need size control

    def hide_edge_controls(self):
        # Hide all Edge controls
        self.name_label.hide()
        self.name_edit.hide()
        self.color_button.hide()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node-Edge Graph")
        self.setGeometry(100, 100, 800, 600)

        self.graph_widget = GraphWidget()
        self.setCentralWidget(self.graph_widget)

        # Create a QDockWidget for the buttons
        dock_widget = QDockWidget("Controls", self)
        dock_widget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        button_widget = QWidget()
        button_layout = QVBoxLayout()

        add_node_button = QPushButton("Add Node")
        add_edge_button = QPushButton("Add Edge")
        self.EditMenu = EditMenu()  # Save reference to node edit menu
        self.EditMenu.graph = self.graph_widget
        add_node_button.clicked.connect(self.add_node)
        add_edge_button.clicked.connect(self.add_edge)

        button_layout.addWidget(self.EditMenu)
        button_layout.addWidget(add_node_button)
        button_layout.addWidget(add_edge_button)
        button_widget.setLayout(button_layout)

        dock_widget.setWidget(button_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)
        self.graph_widget.SelectionChanged.update.append(self.updateSelection)
        self.node_counter = 1  # Initialize node counter
        
    def updateSelection(self):
        self.EditMenu.updateSelection(self.graph_widget.selected)
        
    def add_node(self):
        name = f"v{self.node_counter}"
        self.node_counter += 1
        pos = QPoint(100 + len(self.graph_widget.nodes) * 50, 300)
        self.graph_widget.add_node(name, pos)

    def add_edge(self):
        if len(self.graph_widget.nodes) < 1:
            return

        node_names = [node.name for node in self.graph_widget.nodes]
        node1_name, ok1 = QInputDialog.getItem(self, "Add Edge", "Select first node:", node_names)
        if not ok1 or not node1_name:
            return

        node2_name, ok2 = QInputDialog.getItem(self, "Add Edge", "Select second node:", node_names)
        if not ok2 or not node2_name:
            return

        from_node = next(node for node in self.graph_widget.nodes if node.name == node1_name)
        to_node = next(node for node in self.graph_widget.nodes if node.name == node2_name)
        self.graph_widget.add_edge(from_node, to_node)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
