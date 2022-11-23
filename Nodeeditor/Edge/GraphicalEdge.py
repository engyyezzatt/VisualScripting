# -*- coding: utf-8 -*-
"""
A module containing the Graphics representation of an Edge
"""
from PyQt5.QtWidgets import QGraphicsPathItem, QWidget, QGraphicsItem
from PyQt5.QtGui import QColor, QPen, QPainterPath
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5 import QtCore,QtGui
import math

from Nodeeditor.Edge.GraphicalEdgeTypes import GraphicsEdgePathCurve, GraphicsEdgePathDirect, GraphicsEdgePathSquare


class DrawGraphicalEdge(QGraphicsPathItem):
    """Base class for Graphics Edge"""
    def __init__(self, edge:'Edge', parent:QWidget=None):
        """
        :param edge: reference to :class:`~nodeeditor.node_edge.Edge`
        :type edge: :class:`~nodeeditor.node_edge.Edge`
        :param parent: parent widget
        :type parent: ``QWidget``

        :Instance attributes:

            - **edge** - reference to :class:`~nodeeditor.node_edge.Edge`
            - **posSource** - ``[x, y]`` source position in the `Scene`
            - **posDestination** - ``[x, y]`` destination position in the `Scene`
        """
        super().__init__(parent)

        self.edge = edge

        # create instance of our path class
        self.pathCalculator = self.determineEdgeTypeClass()(self)

        # init our flags
        self._last_selected_state = False
        self.hovered = False

        # init our variables
        self.start_pos = [0, 0]
        self.destination_pos = [200, 100]

        self.initiateAssets()
        self.grEdgeProperties()

    def grEdgeProperties(self):
        """Set up this ``QGraphicsPathItem``"""
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setZValue(-1)

    def initiateAssets(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""
        self.color = QColor("Red")
        self.pen = QPen(self.color)
        self.pen.setWidthF(3.0)

        self.color_selected = QColor("#00ff00")
        self.pen_selected = QPen(self.color_selected)
        self.pen_selected.setWidthF(3.0)

        self.color_hovered = QColor("#00ff00")
        self.pen_hovered = QPen(self.color_hovered)
        self.pen_hovered.setWidthF(5.0)


        self.pen_dragging = QPen(self.color)
        self.pen_dragging.setWidthF(3.0)
        self.pen_dragging.setStyle(Qt.DashLine)

        size = 6.0
        self.arrow = QtGui.QPolygonF()
        self.arrow.append(QtCore.QPointF(-size, size))
        self.arrow.append(QtCore.QPointF(0.0, -size * 1.5))
        self.arrow.append(QtCore.QPointF(size, size))
        self.active = False
        self._highlight = False
        self.color_arrow = QColor("Black")


    def createEdgePathCalculator(self):
        """Create instance of :class:`~nodeeditor.node_graphics_edge_path.GraphicsEdgePathBase`"""
        self.pathCalculator = self.determineEdgeTypeClass()(self)
        return self.pathCalculator

    def determineEdgeTypeClass(self):
        """Decide which GraphicsEdgePath class should be used to calculate path according to edge.edge_type value"""
        from Nodeeditor.Edge.EdgeFunc import EDGE_TYPE_BEZIER, EDGE_TYPE_DIRECT, EDGE_TYPE_SQUARE_LINE
        if self.edge.edge_type == EDGE_TYPE_BEZIER:
            return GraphicsEdgePathCurve
        if self.edge.edge_type == EDGE_TYPE_DIRECT:
            return GraphicsEdgePathDirect
        if self.edge.edge_type == EDGE_TYPE_SQUARE_LINE:
            return GraphicsEdgePathSquare
        else:
            return GraphicsEdgePathCurve

    def makeUnselectable(self):
        """Used for drag edge to disable click detection over this graphics item"""
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setAcceptHoverEvents(False)

    def changeColor(self, color):
        """Change color of the edge from string hex value '#00ff00'"""
        # print("^Called change color to:", color.red(), color.green(), color.blue(), "on edge:", self.edge)
        self.color = QColor(color) if type(color) == str else color
        self.pen = QPen(self.color)
        self.pen.setWidthF(3.0)

    def setColorFromSockets(self) -> bool:
        """Change color according to connected sockets. Returns ``True`` if color can be determined"""
        socket_type_start = self.edge.start_socket.socket_type
        socket_type_end = self.edge.end_socket.socket_type
        if socket_type_start != socket_type_end: return False
        self.changeColor(self.edge.start_socket.grSocket.getSocketColor(socket_type_start))

    def onSelected(self):
        """Our event handling when the edge was selected"""
        self.edge.scene.grScene.itemSelected.emit()

    def doSelect(self, new_state:bool=True):
        """Safe version of selecting the `Graphics Node`. Takes care about the selection state flag used internally

        :param new_state: ``True`` to select, ``False`` to deselect
        :type new_state: ``bool``
        """
        self.setSelected(new_state)
        self._last_selected_state = new_state
        if new_state: self.onSelected()

    def mouseReleaseEvent(self, event):
        """Overridden Qt's method to handle selecting and deselecting this `Graphics Edge`"""
        super().mouseReleaseEvent(event)
        if self._last_selected_state != self.isSelected():
            self.edge.scene.resetLastSelectedStates()
            self._last_selected_state = self.isSelected()
            self.onSelected()

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        """Handle hover effect"""
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        """Handle hover effect"""
        self.hovered = False
        self.update()

    def setSource(self, x:float, y:float):
        """ Set source point

        :param x: x position
        :type x: ``float``
        :param y: y position
        :type y: ``float``
        """
        self.start_pos = [x, y]

    def setDestination(self, x:float, y:float):
        """ Set destination point

        :param x: x position
        :type x: ``float``
        :param y: y position
        :type y: ``float``
        """
        self.destination_pos = [x, y]

    def boundingRect(self) -> QRectF:
        """Defining Qt' bounding rectangle"""
        return self.shape().boundingRect()

    def shape(self) -> QPainterPath:
        """Returns ``QPainterPath`` representation of this `Edge`

        :return: path representation
        :rtype: ``QPainterPath``
        """
        return self.calcPath()

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Qt's overridden method to paint this Graphics Edge. Path calculated
            in :func:`~nodeeditor.node_graphics_edge.QDMGraphicsEdge.calcPath` method"""
        self.setPath(self.calcPath())

        painter.setBrush(Qt.NoBrush)

        if self.hovered and self.edge.end_socket is not None:
            painter.setPen(self.pen_hovered)
            painter.drawPath(self.path())

        if self.edge.end_socket is None:
            painter.setPen(self.pen_dragging)
        else:
            painter.setPen(self.pen if not self.isSelected() else self.pen_selected)

        painter.drawPath(self.path())

        # draw arrow
        if self.start_pos and self.destination_pos:
            cen_x = self.path().pointAtPercent(0.5).x()
            cen_y = self.path().pointAtPercent(0.5).y()
            loc_pt = self.path().pointAtPercent(0.49)
            tgt_pt = self.path().pointAtPercent(0.51)

            dist = math.hypot(tgt_pt.x() - cen_x, tgt_pt.y() - cen_y)
            if dist < 0.5:
                painter.restore()
                return

            self.color.setAlpha(255)
            if self._highlight:
                painter.setBrush(QtGui.QBrush(self.color_arrow.lighter(150)))
            elif self.active or self.isEnabled():
                painter.setBrush(QtGui.QBrush(self.color_arrow.darker(200)))
            else:
                painter.setBrush(QtGui.QBrush(self.color_arrow.darker(130)))

            pen_width = 0.6
            if dist < 1.0:
                pen_width *= (1.0 + dist)

            pen = QtGui.QPen(self.color_arrow, pen_width)
            pen.setCapStyle(QtCore.Qt.RoundCap)
            pen.setJoinStyle(QtCore.Qt.MiterJoin)
            painter.setPen(pen)

            transform = QtGui.QTransform()
            transform.translate(cen_x, cen_y)
            radians = math.atan2(tgt_pt.y() - loc_pt.y(),
                                 tgt_pt.x() - loc_pt.x())
            degrees = math.degrees(radians) - 270
            transform.rotate(degrees)
            if dist < 1.0:
                transform.scale(dist, dist)
            painter.drawPolygon(transform.map(self.arrow))

            # QPaintDevice: Cannot destroy paint device that is being painted.
        painter.restore()

    def intersectsWith(self, p1:QPointF, p2:QPointF) -> bool:
        """Does this Graphics Edge intersect with the line between point A and point B ?

        :param p1: point A
        :type p1: ``QPointF``
        :param p2: point B
        :type p2: ``QPointF``
        :return: ``True`` if this `Graphics Edge` intersects
        :rtype: ``bool``
        """
        cut_path = QPainterPath(p1)
        cut_path.lineTo(p2)
        path = self.calcPath()
        return cut_path.intersects(path)

    def calcPath(self) -> QPainterPath:
        """Will handle drawing QPainterPath from Point A to B. Internally there exist self.pathCalculator which
        is an instance of derived :class:`~nodeeditor.node_graphics_edge_path.GraphicsEdgePathBase` class
        containing the actual `calcPath()` function - computing how the edge should look like.

        :returns: ``QPainterPath`` of the edge connecting `source` and `destination`
        :rtype: ``QPainterPath``
        """
        return self.pathCalculator.calcPath()

    def highlighted(self):
        return self._highlight

