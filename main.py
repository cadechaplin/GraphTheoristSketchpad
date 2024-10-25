import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget, QVBoxLayout, QPushButton, QInputDialog
from PyQt5.QtCore import Qt, QPoint
from graph import GraphWidget
from edit_menu import EditMenu

    
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
        self.EditMenu.bind_graph(self.graph_widget)
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
        self.edge_counter = 1  # Initialize edge counter
        
    def updateSelection(self):
        self.EditMenu.updateSelection(self.graph_widget.selected)
        
    def add_node(self):
        name = f"v{self.node_counter}"
        self.node_counter += 1
        pos = QPoint(100 + len(self.graph_widget.nodes) * 50, 300)
        self.graph_widget.add_node(name, pos)
        self.EditMenu.updateSelection(None)

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
        
        self.graph_widget.add_edge(from_node, to_node, "edge " + str(self.edge_counter), True)
        self.edge_counter += 1
        self.EditMenu.updateSelection(None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
