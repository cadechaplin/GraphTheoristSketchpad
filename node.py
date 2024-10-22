from PyQt5.QtCore import Qt

class Node:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.edges = []
        self.size = 40
        self.fill_color = Qt.lightGray
