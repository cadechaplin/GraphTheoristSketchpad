import sys
from PyQt5.QtWidgets import QGraphicsView, QApplication, QMainWindow, QDockWidget, QWidget, QVBoxLayout, QPushButton, QInputDialog
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QPen, QBrush





from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QApplication
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtGui import QPainter, QPen, QPainterPath
import sys
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QApplication
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPainter, QPen, QBrush, QPainterPath
import sys
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QApplication
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPainter, QPen, QBrush, QPainterPath, QPainterPathStroker
import sys

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QApplication
from PyQt5.QtCore import Qt, QRectF, QPointF, QPoint
from PyQt5.QtGui import QPainter, QPen, QBrush, QPainterPath, QPainterPathStroker
import sys

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QApplication
from PyQt5.QtCore import Qt, QRectF, QPointF, QPoint
from PyQt5.QtGui import QPainter, QPen, QBrush, QPainterPath, QPainterPathStroker
import sys

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QApplication
from PyQt5.QtCore import Qt, QRectF, QPointF, QPoint
from PyQt5.QtGui import QPainter, QPen, QBrush, QPainterPath, QPainterPathStroker
import sys

class Node(QGraphicsItem):
    def __init__(self, name, x, y, size=20):
        super(Node, self).__init__()
        self.name = name
        self.setPos(x, y)
        self.size = size
        self.setAcceptHoverEvents(True)  # Enable hover events

    def boundingRect(self):
        return QRectF(-self.size / 2, -self.size / 2, self.size, self.size)

    def paint(self, painter, option, widget):
        # Draw the node
        painter.setBrush(QBrush(Qt.blue))
        painter.drawEllipse(self.boundingRect())

        # Draw the bounding rectangle
        painter.setPen(QPen(Qt.red, 1, Qt.DashLine))
        painter.drawRect(self.boundingRect())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print(f"Node {self.name} clicked")

    def hoverEnterEvent(self, event):
        print(f"Hover enter on node {self.name}")
        self.update()

    def hoverLeaveEvent(self, event):
        print(f"Hover leave on node {self.name}")
        self.update()

class Edge(QGraphicsItem):
    def __init__(self, name, from_node, to_node):
        super(Edge, self).__init__()
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.setZValue(-1)  # Ensure edges are drawn behind nodes
        self.setAcceptHoverEvents(True)  # Enable hover events

    def boundingRect(self):
        return QRectF(self.from_node.pos(), self.to_node.pos()).normalized().adjusted(-2, -2, 2, 2)

    def shape(self):
        path = QPainterPath()
        path.moveTo(self.from_node.pos())
        path.lineTo(self.to_node.pos())
        stroker = QPainterPathStroker()
        stroker.setWidth(4)  # Set the width of the hitbox
        return stroker.createStroke(path)

    def paint(self, painter, option, widget):
        # Draw the edge
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(self.from_node.pos(), self.to_node.pos())

        # Draw the shape used for hit detection
        painter.setPen(QPen(Qt.red, 1, Qt.DashLine))
        painter.drawPath(self.shape())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print(f"{self.name} from {self.from_node.name} to {self.to_node.name} clicked")

    def hoverEnterEvent(self, event):
        print(f"Hover enter on edge {self.name}")
        self.update()

    def hoverLeaveEvent(self, event):
        print(f"Hover leave on edge {self.name}")
        self.update()

class CurvedEdge(QGraphicsItem):
    def __init__(self, name, from_node, to_node, control_point):
        super(CurvedEdge, self).__init__()
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.control_point = control_point
        self.setZValue(-1)  # Ensure edges are drawn behind nodes
        self.setAcceptHoverEvents(True)  # Enable hover events

    def boundingRect(self):
        path = self._createPath()
        return path.boundingRect().adjusted(-2, -2, 2, 2)  # Adjust to account for line width

    def _createPath(self):
        path = QPainterPath()
        path.moveTo(self.from_node.pos())
        path.quadTo(self.control_point, self.to_node.pos())
        return path

    def shape(self):
        path = self._createPath()
        stroker = QPainterPathStroker()
        stroker.setWidth(4)  # Set the width of the hitbox
        return stroker.createStroke(path)

    def paint(self, painter, option, widget):
        # Draw the curved edge
        painter.setPen(QPen(Qt.black, 2))
        path = self._createPath()
        painter.drawPath(path)

        # Draw the shape used for hit detection
        painter.setPen(QPen(Qt.red, 1, Qt.DashLine))
        painter.drawPath(self.shape())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print(f"{self.name} from {self.from_node.name} to {self.to_node.name} clicked")

    def hoverEnterEvent(self, event):
        print(f"Hover enter on curved edge {self.name}")
        self.update()

    def hoverLeaveEvent(self, event):
        print(f"Hover leave on curved edge {self.name}")
        self.update()

class GraphWidget(QGraphicsView):
    def __init__(self, parent=None):
        super(GraphWidget, self).__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.nodes = []
        self.edges = []

    def add_node(self, name, x, y):
        node = Node(name, x, y)
        self.nodes.append(node)
        self.scene.addItem(node)

    def add_edge(self, name, from_node, to_node, control_point=None):
        if control_point:
            edge = CurvedEdge(name, from_node, to_node, control_point)
        else:
            edge = Edge(name, from_node, to_node)
        self.edges.append(edge)
        self.scene.addItem(edge)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    graph_widget = GraphWidget()
    graph_widget.add_node("Node1", 50, 50)
    graph_widget.add_node("Node2", 150, 150)
    graph_widget.add_edge("straight edge", graph_widget.nodes[0], graph_widget.nodes[1])
    graph_widget.add_edge("curved edge", graph_widget.nodes[1], graph_widget.nodes[0], control_point=QPoint(100, 0))
    graph_widget.show()
    sys.exit(app.exec_())