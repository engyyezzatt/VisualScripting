from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Nodeeditor.SceneFunc import AllSceneFunctions
from Nodeeditor.NodeFunc import AllNodeFunctions
from Nodeeditor.EdgeFunc import AllEdgeFunctions, EDGE_TYPE_CURVE
from Nodeeditor.GraphicalView import DrawGraphicalView


class NodeEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stylesheet_filename = 'qss/nodestyle.qss'
        self.loadStyleSheet(self.stylesheet_filename)

        self.createHomeWidget()

    def createHomeWidget(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # initiate graphics scene
        self.scene = AllSceneFunctions()

        # initiate graphics view
        self.view = DrawGraphicalView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

        self.addNodes()

    def addNodes(self):
        node1 = AllNodeFunctions(self.scene, "My Awesome Node 1", inputs=[0, 0, 0], outputs=[1])
        node2 = AllNodeFunctions(self.scene, "My Awesome Node 2", inputs=[3, 3, 3], outputs=[1])
        node3 = AllNodeFunctions(self.scene, "My Awesome Node 3", inputs=[2, 2, 2], outputs=[1])
        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -150)

        edge1 = AllEdgeFunctions(self.scene, node1.outputs[0], node2.inputs[0], edge_type=EDGE_TYPE_CURVE)
        edge2 = AllEdgeFunctions(self.scene, node2.outputs[0], node3.inputs[0], edge_type=EDGE_TYPE_CURVE)

    def loadStyleSheet(self, filename):
        print('STYLE loading:', filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))
