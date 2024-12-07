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
        self.nodes.graph = self  # Add reference to self in nodes manager
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
        self.onStructureChanged = Event()

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
        self.onStructureChanged.trigger()
        self.update()
        return node
        
    def get_next_available_edge_index(self):
        existing_indices = set()
        for edge in self.edges:
            if edge.name.startswith('edge '):
                try:
                    index = int(edge.name[5:])  # Skip "edge " prefix
                    existing_indices.add(index)
                except ValueError:
                    print("Value Error!")
        
        # Find first available index
        index = 1
        while index in existing_indices:
            index += 1
        return index
        
    def add_edge(self, from_node, to_node, name, directional=False):
        # Always use next available index for edge names, regardless of provided name
        next_index = self.get_next_available_edge_index()
        name = f"edge {next_index}"
        
        # Count edges in both directions, ignoring direction
        existing_edge_count = sum(1 for edge in self.edges 
                                if (edge.from_node == from_node and edge.to_node == to_node) or
                                (edge.from_node == to_node and edge.to_node == from_node) or
                                (edge.from_node == from_node and edge.to_node == from_node) or
                                (edge.from_node == to_node and edge.to_node == to_node))
        
        edge = Edge(from_node, to_node, existing_edge_count + 1, name)
        edge.onChange.update.append(self.update)
        viewModel = EdgeViewModel(edge, self.nodes)
        edge.viewModel = viewModel
        self.scene.addItem(viewModel)
        edge.directional = directional # Set the directionality
        self.edges.append(edge)
        self.edge_count += 1
        self.update_counters()
        self.onStructureChanged.trigger()
        self.SelectionChanged.trigger()
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
    

    def removeItem(self, item):
        if isinstance(item, Node):
            # Deselect the node if it's selected
            if self.nodes.selected == item:
                self.nodes.setSelected(None)
            
            # Remove connected edges
            edges_to_remove = [edge for edge in self.edges[:] 
                               if edge.from_node == item or edge.to_node == item]
            for edge in edges_to_remove:
                self.removeItem(edge)  # Recursive call to handle edge removal
            
            # Remove the node
            if item.viewModel:
                self.scene.removeItem(item.viewModel)
            self.nodes.remove(item)
            self.node_count -= 1  # Decrement node count
            
        elif isinstance(item, Edge):
            # Deselect the edge if it's selected
            if self.selected == item:
                self.selected = None
            if item.viewModel:
                item.viewModel.selected = False
                self.scene.removeItem(item.viewModel)
            self.edges.remove(item)
            item.onDelete.trigger()
            self.edge_count -= 1  # Decrement edge count
        
        # Update counters and UI
        self.update_counters()
        self.onStructureChanged.trigger()
        self.update()
        
    def get_next_available_node_index(self):
        existing_indices = set()
        for node in self.nodes:
            if node.name.startswith('v'):
                try:
                    index = int(node.name[1:])
                    existing_indices.add(index)
                except ValueError:
                    print("Value Error!")
        
        # Find first available index
        index = 0
        while index in existing_indices:
            index += 1
        return index





