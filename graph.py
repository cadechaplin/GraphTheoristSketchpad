

import math
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsTextItem
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

        # Add counter text items
        self.node_count_text = QGraphicsTextItem()
        self.edge_count_text = QGraphicsTextItem()
        self.scene.addItem(self.node_count_text)
        self.scene.addItem(self.edge_count_text)

        # Add node and edge count items
        self.node_count = 0
        self.edge_count = 0
        
        # Position text items in top-left, and make counter text items stay on top of other elements
        self.node_count_text.setZValue(1000)
        self.edge_count_text.setZValue(1000)
        
        # Force counter items to stay in viewport
        self.node_count_text.setFlag(QGraphicsTextItem.ItemIgnoresTransformations)
        self.edge_count_text.setFlag(QGraphicsTextItem.ItemIgnoresTransformations)
        self.update_counters()

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update counter positions
        self.updateCounterPositions()
        
    def viewportEvent(self, event):
        result = super().viewportEvent(event)
        # Keep counters in fixed position
        self.updateCounterPositions()
        return result
        
    def updateCounterPositions(self):
        # Convert viewport coordinates to scene coordinates
        self.node_count_text.setPos(self.mapToScene(10, 10))
        self.edge_count_text.setPos(self.mapToScene(10, 30))

    def update_counters(self):
        self.node_count_text.setPlainText(f"Nodes: {self.node_count}")
        self.edge_count_text.setPlainText(f"Edges: {self.edge_count}")

    def add_node(self, name, pos):
        node = Node(name, pos)
        viewModel = NodeViewModel(node, self.nodes)
        node.viewModel = viewModel
        viewModel.setPos(pos)
        self.nodes.append(node)
        node.onChange.update.append(self.update)
        self.scene.addItem(viewModel)
        self.node_count += 1
        self.update_counters()
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
        self.edge_count += 1
        self.update_counters()
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
    
    

    
            
