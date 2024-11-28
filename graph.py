

import math
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QPainterPath
from events import Event
from node import Node
from nodeViewModel import NodeViewModel
from edge import Edge
from edgeViewModel import EdgeViewModel
from selectionManager import selectionManager

class GraphWidget(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.nodes = selectionManager()
        self.SelectionChanged = Event()
        self.nodes.onSelectionChanged.update.append(self.SelectionChanged.trigger)
        self.edges = []
        self.dragging_node = None
        self.selected = None
        
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.node_counter = 1  # Initialize node counter
        self.edge_counter = 1  # Initialize edge counter
        self.countLookup = {}  # Dictionary to store edge counts for each node pair

    def add_node(self, name, pos):
        node = Node(name, pos)
        viewModel = NodeViewModel(node, self.nodes)
        node.viewModel = viewModel
        self.nodes.append(node)
        node.onChange.update.append(self.update)
        self.scene.addItem(viewModel)
        self.update()
        
        
        
    def add_edge(self, from_node, to_node, name, directional=False):
        # Count edges in both directions, ignoring direction
        
        existing_edge_count = sum(1 for edge in self.edges 
                                if (edge.from_node == from_node and edge.to_node == to_node) or  # Forward edges
                                (edge.from_node == to_node and edge.to_node == from_node) or  # Backward edges
                                (edge.from_node == from_node and edge.to_node == from_node) or  # Self-loops from source
                                (edge.from_node == to_node and edge.to_node == to_node))  # Self-loops from target
        
        edge = Edge(from_node, to_node, existing_edge_count + 1, name)
        edge.onChange.update.append(self.update)
        viewModel = EdgeViewModel(edge, self.nodes)
        edge.viewModel = viewModel
        self.scene.addItem(viewModel)
        edge.directional = directional
        self.edges.append(edge)
        self.update()
    
    '''
    
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
        


    


     
   
    
    
    
    '''
    
    

    
            
