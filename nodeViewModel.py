import sys
from PyQt5.QtCore import Qt, QRectF, QPointF, QPoint, QEvent
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsTextItem, QApplication
from PyQt5.QtGui import QPainter, QPen, QBrush, QPainterPath, QPainterPathStroker, QColor

class NodeViewModel(QGraphicsItem):
    def __init__(self, node, selectionList):
        super(NodeViewModel, self).__init__()
        self.__node = node
        self.__node.onChange.update.append(self.update)
        self.__node.onDelete.update.append(self.onDelete)
        self.setAcceptHoverEvents(True)  # Enable hover events
        self.setFlag(QGraphicsItem.ItemIsMovable, True)  # Enable item movement
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)  # Enable geometry change notifications
        self.dColor = QColor(Qt.blue)
        self.sColor = QColor(Qt.red)
        self.hoverColor = self.dColor.lighter(125)  # Color when hovering
        self.selected = False
        self.hovering = False  # Initialize hovering state
        self.dragging = False  # Initialize dragging state
        self.selectionList = selectionList

        # Add label
        self.label = QGraphicsTextItem(self.__node.name, self)
        self.label.setDefaultTextColor(Qt.black)
        self.update_label_position()
    
    def boundingRect(self):
        return QRectF(-self.__node.getSize() / 2, -self.__node.getSize() / 2, self.__node.getSize(), self.__node.getSize())
    
    def paint(self, painter, option, widget):
        # Ensure the label position is updated
        self.update_label_position()

        # Set the brush color based on the state
        if self.hovering:
            painter.setBrush(QBrush(self.hoverColor))
        else: 
            painter.setBrush(QBrush(self.dColor))
        if self.isSelected():
            painter.setPen(QPen(self.sColor, 2))
        else:
            painter.setPen(QPen(Qt.black, 2))
        
        # Draw the node
        painter.drawEllipse(self.boundingRect())

    def shape(self):
        path = QPainterPath()
        path.addEllipse(self.boundingRect())
        return path
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.setCursor(Qt.ClosedHandCursor)
            self.update()
        super(NodeViewModel, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging:
            new_pos = event.scenePos()
            self.__node.updatePos(new_pos)
            self.setPos(new_pos)
            self.update()
            # Force the scene to update
            if self.scene():
                self.scene().update()
        super(NodeViewModel, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.setCursor(Qt.ArrowCursor)
            self.update()
        super(NodeViewModel, self).mouseReleaseEvent(event)
        
    def mouseDoubleClickEvent(self, event):
        # First properly handle edge deselection
        if hasattr(self.selectionList, 'graph'):
            if self.selectionList.graph.selected:
                old_edge = self.selectionList.graph.selected
                old_edge.viewModel.selected = False
                old_edge.viewModel.update()
                self.selectionList.graph.selected = None
                
        # Then handle node selection/deselection
        if self.selected:
            self.selectionList.setSelected(None)
            self.selected = False
        else:
            self.selectionList.setSelected(self.__node)
            self.selected = True
        
        self.update()
        super().mouseDoubleClickEvent(event)

    def hoverEnterEvent(self, event):
        self.hovering = True
        self.update()

    def hoverLeaveEvent(self, event):
        self.hovering = False
        self.update()
    
    def isSelected(self):
        return self.selected

    def update_label_position(self):
        # Center the label on the x-axis and position it above the node
        self.label.setPlainText(self.__node.name)
        label_rect = self.label.boundingRect()
        node_rect = self.boundingRect()
        self.label.setPos(node_rect.center().x() - label_rect.width() / 2, node_rect.top() - label_rect.height())
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            self.update_label_position()
        return super(NodeViewModel, self).itemChange(change, value)
    
    def onDelete(self):
        scene = self.scene()
        if scene:
            scene.removeItem(self)
            scene.update()
