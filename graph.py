

import math
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QPainterPath
from events import Event
from node import Node
from nodeViewModel import NodeViewModel
from edge import Edge
from edgeViewModel import EdgeViewModel

class GraphWidget(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.dragging_node = None
        self.selected = None
        self.SelectionChanged = Event()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

    def add_node(self, name, pos):
        node = Node(name, pos)
        viewModel = NodeViewModel(node)
        self.nodes.append(node)
        self.scene.addItem(viewModel)
        self.update()
        
        
    def add_edge(self, from_node, to_node, name, directional=False):
        existing_edge_count = 0
        for existing_edge in self.edges:
            if existing_edge.from_node == from_node and existing_edge.to_node == to_node:
                if existing_edge_count < existing_edge.count:
                    existing_edge_count = existing_edge.count
        edge = Edge(from_node, to_node, existing_edge_count+1, name)
        viewModel = EdgeViewModel(edge)
        self.scene.addItem(viewModel)
        edge.directional = directional
        '''
        from_node.edges.append(edge)
        to_node.edges.append(edge)
        '''
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
    
    

    
            
