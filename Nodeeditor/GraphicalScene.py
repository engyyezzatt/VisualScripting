import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class DrawGraphicalScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.scene = scene

        # settings
        self.gridSize = 20
        self.gridSquares = 5

        self.color_background = QColor("#393939")
        self.setBackgroundBrush(self.color_background)

        self.color_light = QColor("#2f2f2f")
        self.pen_light = QPen(self.color_light)
        self.pen_light.setWidth(1)

        self.color_dark = QColor("#292929")
        self.pen_dark = QPen(self.color_dark)
        self.pen_dark.setWidth(2)

    def setGrScene(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # here we create our grid
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)

        # compute all lines to be drawn
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.gridSize):
            if (x % (self.gridSize * self.gridSquares) != 0):
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.gridSize):
            if (y % (self.gridSize * self.gridSquares) != 0):
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

        # draw the lines
        painter.setPen(self.pen_light)
        painter.drawLines(*lines_light)

        painter.setPen(self.pen_dark)
        painter.drawLines(*lines_dark)
