from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *



class DrawGraphicalNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.content = self.node.content

        self.width = 180
        self.height = 240
        self.edge_size = 10
        self.title_height = 24
        self.padding = 4

        self.pen_default = QPen(QColor("#7F000000"))
        self.pen_selected = QPen(QColor("#FFFFA637"))

        self.brush_title = QBrush(QColor("#FF313131"))
        self.brush_background = QBrush(QColor("#E3212121"))

        # init title
        self.title_color = Qt.white
        self.title_font = QFont("Ubuntu", 10)
        self.titleProperties()
        self.title = self.node.title

        self.wasMoved = False

        # initiate sockets
        self.initSockets()

        # initiate content
        self.initiateNodeContent()

        #initiateMoving
        self.nodeProperties()

    @property
    def title(self): return self._title
    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def titleProperties(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self.title_color)
        self.title_item.setFont(self.title_font)
        self.title_item.setPos(self.padding, 0)
        self.title_item.setTextWidth( self.width - 2 * self.padding )

    def initiateNodeContent(self):
        self.graphical_node_content = QGraphicsProxyWidget(self)
        self.content.setGeometry(self.edge_size, self.title_height + self.edge_size,
                                 self.width - 2 * self.edge_size, self.height - 2 * self.edge_size - self.title_height)
        self.graphical_node_content.setWidget(self.content)

    def boundingRect(self):
        return QRectF(0,0,self.width,self.height).normalized()

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0,0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush_title)
        painter.drawPath(path_title.simplified())

        # Draw Content Widget
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self.pen_default if not self.isSelected() else self.pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())

    def nodeProperties(self):
            self.setFlag(QGraphicsItem.ItemIsSelectable)
            self.setFlag(QGraphicsItem.ItemIsMovable)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        # optimize me! just update the selected nodes
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()
        self.wasMoved = True

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        if self.wasMoved:
            self.wasMoved = False
            self.node.scene.history.storeHistory("Node moved", setModified=True)

    def initSockets(self):
        pass