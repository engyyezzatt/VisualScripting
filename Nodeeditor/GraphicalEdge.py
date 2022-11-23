import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui,QtCore
from Nodeeditor.SocketFunc import *




class DrawGraphicalEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)


        self.edge = edge

        self.color = QColor("#001000")
        self.pen = QPen(self.color)
        self.pen.setWidthF(2.0)

        self.pen_dragging = QPen(self.color)
        self.pen_dragging.setWidthF(2.0)
        self.pen_dragging.setStyle(Qt.DashLine)

        self.color_selected = QColor("#00ff00")
        self.pen_selected = QPen(self.color_selected)
        self.pen_selected.setWidthF(2.0)

        size = 6.0
        self.arrow = QtGui.QPolygonF()
        self.arrow.append(QtCore.QPointF(-size, size))
        self.arrow.append(QtCore.QPointF(0.0, -size * 1.5))
        self.arrow.append(QtCore.QPointF(size, size))
        self.active = False
        self._highlight = False

        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.setZValue(-1)

        self.start_pos = [0, 0]
        self.destination_pos = [200, 100]

    def setSource(self, x, y):
        self.start_pos = [x, y]

    def setDestination(self, x, y):
        self.destination_pos = [x, y]

    def boundingRect(self):
        return self.shape().boundingRect()

    def shape(self):
        return self.calcPath()

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.setPath(self.calcPath())

        if self.edge.end_socket is None:
            painter.setPen(self.pen_dragging)
        else:
            painter.setPen(self.pen if not self.isSelected() else self.pen_selected)
        painter.setBrush(Qt.NoBrush)
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
                painter.setBrush(QtGui.QBrush(self.color.lighter(150)))
            elif self.active or self.isEnabled():
                painter.setBrush(QtGui.QBrush(self.color.darker(200)))
            else:
                painter.setBrush(QtGui.QBrush(self.color.darker(130)))

            pen_width = 0.6
            if dist < 1.0:
                pen_width *= (1.0 + dist)

            pen = QtGui.QPen(self.color, pen_width)
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


    def intersectsWith(self, p1, p2):
        cut_path = QPainterPath(p1)
        cut_path.lineTo(p2)
        path = self.calcPath()
        return cut_path.intersects(path)

    def calcPath(self):
        """ Will handle drawing QPainterPath from Point A to B """
        raise NotImplemented("This method has to be overriden in a child class")

    def highlight(self):
        self._highlight = True
        color = QtGui.QColor("Red")
        pen = QtGui.QPen("Green")
        self.setPen(pen)

    def highlighted(self):
        return self._highlight


class GraphicalEdgeDirect(DrawGraphicalEdge):
    def calcPath(self):
        path = QPainterPath(QPointF(self.start_pos[0], self.start_pos[1]))
        path.lineTo(self.destination_pos[0], self.destination_pos[1])
        return path

#7d yktb comment tfsely el code da by3ml eh
class GraphicalEdgeCurve(DrawGraphicalEdge):
    def calcPath(self):
        s = self.start_pos
        d = self.destination_pos
        dist = (d[0] - s[0]) * 0.5

        cpx_s = +dist
        cpx_d = -dist
        cpy_s = 0
        cpy_d = 0

        EDGE_CP_ROUNDNESS = 100

        if self.edge.start_socket is not None:
            sspos = self.edge.start_socket.position

            if (s[0] > d[0] and sspos in (RIGHT_TOP, RIGHT_BOTTOM)) or (s[0] < d[0] and sspos in (LEFT_BOTTOM, LEFT_TOP)):
                cpx_d *= -1
                cpx_s *= -1
                cpy_d = ((s[1] - d[1]) / math.fabs((s[1] - d[1]) if (s[1] - d[1]) != 0 else 0.00001)) * EDGE_CP_ROUNDNESS
                cpy_s = ((d[1] - s[1]) / math.fabs((d[1] - s[1]) if (d[1] - s[1]) != 0 else 0.00001)) * EDGE_CP_ROUNDNESS

        path = QPainterPath(QPointF(self.start_pos[0], self.start_pos[1]))
        path.cubicTo(s[0] + cpx_s, s[1] + cpy_s, d[0] + cpx_d, d[1] + cpy_d, self.destination_pos[0], self.destination_pos[1])

        return path

