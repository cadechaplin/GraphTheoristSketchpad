import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget, QVBoxLayout, QPushButton, QInputDialog
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen

class Node:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.edges = []

class Edge:
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node

class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.dragging_node = None

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
        painter = QPainter(self)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        for edge in self.edges:
            if edge.from_node.pos == edge.to_node.pos:
                offset = QPoint(20, 20)
                painter.drawEllipse(edge.from_node.pos + offset, 20, 20)
            else:
                painter.drawLine(edge.from_node.pos, edge.to_node.pos)

        for node in self.nodes:
            painter.setBrush(Qt.lightGray)
            painter.drawEllipse(node.pos, 20, 20)
            painter.drawText(node.pos, node.name)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            for node in self.nodes:
                if (node.pos - event.pos()).manhattanLength() < 20:
                    self.dragging_node = node
                    break

    def mouseMoveEvent(self, event):
        if self.dragging_node:
            self.dragging_node.pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging_node = None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node-Edge Graph")
        self.setGeometry(100, 100, 800, 600)

        self.graph_widget = GraphWidget()
        self.setCentralWidget(self.graph_widget)

        # Create a QDockWidget for the buttons
        dock_widget = QDockWidget("Controls", self)
        button_widget = QWidget()
        button_layout = QVBoxLayout()

        add_node_button = QPushButton("Add Node")
        add_edge_button = QPushButton("Add Edge")

        add_node_button.clicked.connect(self.add_node)
        add_edge_button.clicked.connect(self.add_edge)

        button_layout.addWidget(add_node_button)
        button_layout.addWidget(add_edge_button)
        button_widget.setLayout(button_layout)

        dock_widget.setWidget(button_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)

        self.node_counter = 1  # Initialize node counter

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