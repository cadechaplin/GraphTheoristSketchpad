from PyQt5.QtCore import Qt
from events import Event
class Node:
    def __init__(self, name, pos):
        self.viewModel = None
        self.name = name
        self.__pos = pos
        self.__edges = [] # List to track connected edges
        self.__size = 40
        # Change event to handle updates, might be better as a pyqt signal
        self.onChange = Event()
        # Delete event to handle deletion
        self.onDelete = Event()
    def addEdge(self, edge):
        if edge not in self.__edges:
            self.__edges.append(edge)
    
    def removeEdge(self, edge):
        if edge in self.__edges:
            self.__edges.remove(edge)
            
    def getEdges(self):
        return self.__edges
    
    def getRadius(self):
        return self.size / 2
    
    def updatePos(self, pos):
        self.__pos = pos
        self.onChange.trigger()

    def getPos(self):   
        return self.__pos
    
    def updateSize(self, size):
        self.__size = size    
        self.onChange.trigger()

    def getSize(self):
        return self.__size
     