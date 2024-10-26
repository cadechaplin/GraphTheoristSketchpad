from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainterPath, QPainterPathStroker, QPen
from PyQt5.QtCore import Qt


class EdgeViewModel(QGraphicsItem):
    def __init__(self, edge):
        super(EdgeViewModel, self).__init__()
        self.__edge = edge
        self.__edge.from_node.onChange.update.append(self.update)
        self.__edge.to_node.onChange.update.append(self.update)
        self.setZValue(-1)  # Ensure edges are drawn behind nodes
        self.setAcceptHoverEvents(True)  # Enable hover events
        self.__edge.onChange.update.append(self.update)
        self.__edge.onDelete.update.append(self.onDelete)

    def boundingRect(self):
        path = self._createPath()
        return path.boundingRect().adjusted(-2, -2, 2, 2)  # Adjust to account for line width

    def _createPath(self):
        path = QPainterPath()
        path.moveTo(self.__edge.from_node.getPos())
        path.quadTo(self.__edge.getControlPoint(), self.__edge.to_node.getPos())
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
            print(f"{self.__edge.name} from {self.__edge.from_node.name} to {self.__edge.to_node.name} clicked")

    def hoverEnterEvent(self, event):
        print(f"Hover enter on curved edge {self.__edge.name}")
        self.hover = True
        self.update()

    def hoverLeaveEvent(self, event):
        print(f"Hover leave on curved edge {self.__edge.name}")
        self.hover = False
        self.update()
    
    def onDelete(self):
        scene = self.scene()
        if scene:
            scene.removeItem(self)
            scene.update()