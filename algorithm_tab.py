from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSpinBox, QLabel
from PyQt5.QtCore import QPointF
import math

class AlgorithmTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Create controls for grid generation
        grid_label = QLabel("Grid Generator:")
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(1, 10)
        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(1, 10)
        self.create_grid_btn = QPushButton("Create Grid")
        self.create_grid_btn.clicked.connect(self.create_grid)
        
        # Create controls for cycle generation
        cycle_label = QLabel("Cycle Generator:")
        self.vertices_spin = QSpinBox()
        self.vertices_spin.setRange(3, 20)
        self.create_cycle_btn = QPushButton("Create Cycle")
        self.create_cycle_btn.clicked.connect(self.create_cycle)
        
        # Add widgets to layout
        layout.addWidget(grid_label)
        layout.addWidget(QLabel("Rows:"))
        layout.addWidget(self.rows_spin)
        layout.addWidget(QLabel("Columns:"))
        layout.addWidget(self.cols_spin)
        layout.addWidget(self.create_grid_btn)
        layout.addWidget(cycle_label)
        layout.addWidget(QLabel("Vertices:"))
        layout.addWidget(self.vertices_spin)
        layout.addWidget(self.create_cycle_btn)
        
        self.graph = None

    def bind_graph(self, graph):
        self.graph = graph

    def create_grid(self):
        if not self.graph:
            return
            
        rows = self.rows_spin.value()
        cols = self.cols_spin.value()
        spacing = 100
        
        # Create nodes
        nodes = {}  # Using dictionary to store node references
        for i in range(rows):
            for j in range(cols):
                index = self.graph.get_next_available_node_index()
                name = f"v{index}"
                pos = QPointF(j * spacing, i * spacing)
                node = self.graph.add_node(name, pos)
                nodes[name] = node
        
        # Create edges
        node_names = sorted(nodes.keys(), key=lambda x: int(x[1:]))  # Sort by index
        grid_width = cols
        for i, current_name in enumerate(node_names):
            # Horizontal edges
            if (i + 1) % grid_width != 0:  # If not last in row
                next_name = node_names[i + 1]
                self.graph.add_edge(nodes[current_name], nodes[next_name], "edge 0", False)  # Use "edge 0" as placeholder
            # Vertical edges
            if i + grid_width < len(node_names):  # If not in last row
                below_name = node_names[i + grid_width]
                self.graph.add_edge(nodes[current_name], nodes[below_name], "edge 0", False)  # Use "edge 0" as placeholder

    def create_cycle(self):
        if not self.graph:
            return
            
        n = self.vertices_spin.value()
        radius = 200
        center = QPointF(0, 0)
        
        # Create nodes in a circle
        nodes = {}  # Using dictionary to store node references
        for i in range(n):
            index = self.graph.get_next_available_node_index()
            name = f"v{index}"
            angle = 2 * math.pi * i / n
            pos = QPointF(center.x() + radius * math.cos(angle),
                         center.y() + radius * math.sin(angle))
            node = self.graph.add_node(name, pos)
            nodes[name] = node
        
        # Create edges between consecutive nodes
        node_names = sorted(nodes.keys(), key=lambda x: int(x[1:]))  # Sort by index
        for i in range(len(node_names)):
            current_name = node_names[i]
            next_name = node_names[(i + 1) % n]
            self.graph.add_edge(nodes[current_name], nodes[next_name], "edge 0", False)  # Use "edge 0" as placeholder