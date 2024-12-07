from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainterPath, QPainterPathStroker, QPen, QPolygonF, QBrush
from PyQt5.QtCore import Qt, QPointF
import math

class EdgeViewModel(QGraphicsItem):
    def __init__(self, edge, selectionList):
        super(EdgeViewModel, self).__init__()
        self.viewModel = None
        self.__edge = edge
        self.__edge.from_node.onChange.update.append(self.update)
        self.__edge.to_node.onChange.update.append(self.update)
        self.setZValue(-1)  # Ensure edges are drawn behind nodes
        self.setAcceptHoverEvents(True)  # Enable hover events
        self.__edge.onChange.update.append(self.update)
        self.__edge.onDelete.update.append(self.onDelete)
        self.selected = False
        self.selectionList = selectionList

    def boundingRect(self):
        path = self._createPath()
        return path.boundingRect().adjusted(-2, -2, 2, 2)  # Adjust to account for line width

    def _createPath(self):
        path = QPainterPath()
        if self.__edge.from_node == self.__edge.to_node:
            # Get node properties
            node_pos = self.__edge.from_node.getPos()
            node_size = self.__edge.from_node.getSize()
            count = self.__edge.getCount() - 1  # Adjust for multiple self-loops
            
            # Make radius much larger so loop extends beyond node
            radius = node_size * (3 + 0.8 *  1.5 * count)  # Increased multiplier from 1.5 to 3
            base_angle = math.pi/6 + (math.pi/8 )  # 30 degrees + offset for each loop
            
            # Calculate start and end points on node circumference
            start_point = QPointF(
                node_pos.x() + (node_size/2) * math.cos(-base_angle),
                node_pos.y() + (node_size/2) * math.sin(-base_angle)
            )
            end_point = QPointF(
                node_pos.x() + (node_size/2) * math.cos(base_angle),
                node_pos.y() + (node_size/2) * math.sin(base_angle)
            )
            
            # Calculate control points for smooth curve with larger radius
            control1 = QPointF(
                start_point.x() + radius * math.cos(-base_angle - math.pi/6),
                start_point.y() + radius * math.sin(-base_angle - math.pi/6)
            )
            control2 = QPointF(
                end_point.x() + radius * math.cos(base_angle + math.pi/6),
                end_point.y() + radius * math.sin(base_angle + math.pi/6)
            )
            
            path.moveTo(start_point)
            path.cubicTo(control1, control2, end_point)
        else:
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
        if self.selected:
            pen = QPen(Qt.red, 2)
        else:
            pen = QPen(Qt.black, 2)
        path = self._createPath()
        
        painter.setPen(pen)
        painter.drawPath(path)

        # Draw the arrowhead
        if self.__edge.directional and self.__edge.from_node != self.__edge.to_node:
            self._drawArrowhead(painter, path)

    def _calculate_intersection_point(self, center, radius, point):
        # Calculate direction vector from center to point
        dx = point.x() - center.x()
        dy = point.y() - center.y()
        
        # Calculate distance
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Normalize direction vector
        dx = dx / distance
        dy = dy / distance
        
        # Calculate intersection point
        intersection_x = center.x() + dx * radius
        intersection_y = center.y() + dy * radius
        
        return QPointF(intersection_x, intersection_y)

    def _drawArrowhead(self, painter, path):
        # Get end points and calculate direction
        end_point = self.__edge.to_node.getPos()
        t = 0.95  # Get a point slightly before the end for direction
        direction_point = path.pointAtPercent(t)
        
        # Calculate the intersection point with the circular node
        node_radius = self.__edge.to_node.getSize() / 2
        intersection = self._calculate_intersection_point(end_point, node_radius, direction_point)
        
        # Calculate the direction vector from direction point to intersection
        dx = direction_point.x() - intersection.x()  # Reversed to get correct direction
        dy = direction_point.y() - intersection.y()
        angle = math.atan2(dy, dx)
        
        # Arrow dimensions
        arrow_length = 10
        arrow_width = 6
        
        # The tip is at the intersection point
        tip = intersection
        
        # Base points are now calculated in front of the intersection point
        left_base = QPointF(
            tip.x() - math.cos(angle + math.pi * 0.2) * arrow_length,
            tip.y() - math.sin(angle + math.pi * 0.2) * arrow_length
        )
        
        right_base = QPointF(
            tip.x() - math.cos(angle - math.pi * 0.2) * arrow_length,
            tip.y() - math.sin(angle - math.pi * 0.2) * arrow_length
        )
        
        # Create and draw the arrowhead
        arrow_head = QPolygonF([tip, left_base, right_base])
        painter.setBrush(QBrush(Qt.black))
        painter.drawPolygon(arrow_head)
        
    def mouseDoubleClickEvent(self, event):
        if hasattr(self.selectionList, 'graph'):
            graph = self.selectionList.graph
            
            # If this edge is already selected, deselect it
            if graph.selected == self.__edge:
                self.selected = False
                graph.selected = None
                self.update()
                graph.SelectionChanged.trigger()
                return super().mouseDoubleClickEvent(event)
            
            # Clear node selection first
            graph.nodes.setSelected(None)
            
            # Clear any previous edge selection
            if graph.selected:
                graph.selected.viewModel.selected = False
                graph.selected.viewModel.update()
            
            # Set new edge selection
            self.selected = True
            graph.selected = self.__edge
            self.update()
            
            graph.SelectionChanged.trigger()
        
        super().mouseDoubleClickEvent(event)

    
    def onDelete(self):
        scene = self.scene()
        if scene:
            scene.removeItem(self)
            scene.update()