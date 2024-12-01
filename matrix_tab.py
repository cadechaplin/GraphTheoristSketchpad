from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton
import numpy as np

class MatrixTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Create matrix displays
        self.adj_label = QLabel("Adjacency Matrix:")
        self.adj_matrix = QTableWidget()
        self.lap_label = QLabel("Laplacian Matrix:")
        self.lap_matrix = QTableWidget()
        
        # Create refresh button
        self.refresh_btn = QPushButton("Refresh Matrices")
        self.refresh_btn.clicked.connect(self.refresh_matrices)
        
        # Add widgets to layout
        layout.addWidget(self.adj_label)
        layout.addWidget(self.adj_matrix)
        layout.addWidget(self.lap_label)
        layout.addWidget(self.lap_matrix)
        layout.addWidget(self.refresh_btn)
        
        self.selection_manager = None
        self.graph = None

    def bind_graph(self, graph):
        self.graph = graph
        # Listen for any changes in the graph structure
        self.graph.nodes.onSelectionChanged.update.append(self.refresh_matrices)
        self.graph.SelectionChanged.update.append(self.refresh_matrices)
        self.graph.onStructureChanged.update.append(self.refresh_matrices)  # This event should be triggered when nodes/edges are added/removed
        self.refresh_matrices()

    def refresh_matrices(self):
        if not self.graph:
            return
            
        # Get all nodes from the graph
        all_nodes = self.graph.nodes
        if not all_nodes:
            return

        n = len(all_nodes)
        
        # Setup matrices
        self.adj_matrix.setRowCount(n)
        self.adj_matrix.setColumnCount(n)
        self.lap_matrix.setRowCount(n)
        self.lap_matrix.setColumnCount(n)
        
        # Create adjacency matrix
        adj = np.zeros((n, n))
        for edge in self.graph.edges:
            if edge.from_node in all_nodes and edge.to_node in all_nodes:
                i = all_nodes.index(edge.from_node)
                j = all_nodes.index(edge.to_node)
                adj[i][j] = 1
                if not edge.directional:
                    adj[j][i] = 1
                
        # Create Laplacian matrix
        degree = np.diag(np.sum(adj, axis=1))
        lap = degree - adj
        
        # Update displays
        for i in range(n):
            self.adj_matrix.setHorizontalHeaderItem(i, QTableWidgetItem(all_nodes[i].name))
            self.adj_matrix.setVerticalHeaderItem(i, QTableWidgetItem(all_nodes[i].name))
            self.lap_matrix.setHorizontalHeaderItem(i, QTableWidgetItem(all_nodes[i].name))
            self.lap_matrix.setVerticalHeaderItem(i, QTableWidgetItem(all_nodes[i].name))
            for j in range(n):
                self.adj_matrix.setItem(i, j, QTableWidgetItem(str(int(adj[i][j]))))
                self.lap_matrix.setItem(i, j, QTableWidgetItem(str(int(lap[i][j]))))