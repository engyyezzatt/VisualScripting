# -*- coding: utf-8 -*-
"""
A module containing Graphics representation of a :class:`~nodeeditor.node_socket.Socket`
"""
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QRectF

SOCKET_COLORS = [
    QColor("#F87217"),
    QColor("#F87217"),
    QColor("#F87217"),
    QColor("#F87217"),
    QColor("#F87217"),
    QColor("#F87217"),
    QColor("#F87217"),
    QColor("#F87217"),
    QColor("#F87217"),
    QColor("#F87217"),
    QColor("#F87217"),
    QColor("#F87217"),
    QColor("#F87217"),
    QColor("#F87217"),
]

class DrawGraphicalSocket(QGraphicsItem):
    """Class representing Graphic `Socket` in ``QGraphicsScene``"""
    def __init__(self, socket:'Socket'):
        """
        :param socket: reference to :class:`~nodeeditor.node_socket.Socket`
        :type socket: :class:`~nodeeditor.node_socket.Socket`
        """
        super().__init__(socket.node.grNode)

        self.socket = socket

        self.isHighlighted = False

        self.radius = 6

        self.classAssets()

    @property
    def socket_type(self):
        return self.socket.socket_type

    def getSocketColor(self, key):
        """Returns the ``QColor`` for this ``key``"""
        if type(key) == int: return SOCKET_COLORS[key]
        elif type(key) == str: return QColor(key)
        return Qt.transparent

    def changeSocketType(self):
        """Change the Socket Type"""
        self.color_background = self.getSocketColor(self.socket_type)
        self.brush_background = QBrush(self.color_background)
        # print("Socket changed to:", self._color_background.getRgbF())
        self.update()

    def classAssets(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""

        # determine socket color
        self.color_background = self.getSocketColor(self.socket_type)
        self.brush_background = QBrush(self.color_background)


        self.outline_color = QColor("#FF000000")
        self.outline_pen = QPen(self.outline_color)
        self.outline_width = 0
        self.outline_pen.setWidthF(self.outline_width)

        self.color_highlight = QColor("#FF37A6FF")
        self.pen_highlight = QPen(self.color_highlight)
        self.pen_highlight.setWidthF(2.0)


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Painting a circle"""
        painter.setBrush(self.brush_background)
        painter.setPen(self.outline_pen if not self.isHighlighted else self.pen_highlight)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def boundingRect(self) -> QRectF:
        """Defining Qt' bounding rectangle"""
        return QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        )
