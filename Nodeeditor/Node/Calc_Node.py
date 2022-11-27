from PyQt5.QtWidgets import *
from Nodeeditor.Node.NodeFunc import AllNodeFunctions
from Nodeeditor.SystemProperties.HomeWidget import *
from Nodeeditor.Node.GraphicalNode import *
from Nodeeditor.Node.ContentWidgetFunc import AllContentWidgetFunctions
from Nodeeditor.Node.GraphicalNode import DrawGraphicalNode

class CalcGraphicalNode(DrawGraphicalNode):
    def initSizes(self):
        """Set up internal attributes like `width`, `height`, etc."""
        super().initSizes()
        self.width = 160.0
        self.height = 74.0
        self.edge_roundness = 6.0
        self.edge_padding = 0.0
        self.title_horizontal_padding = 8.0
        self.title_vertical_padding = 10.0


class CalcContent(AllContentWidgetFunctions):
    def initUI(self):
        lbl = QLabel("",self)

class CalcNode(AllNodeFunctions):
    def __init__(self,scene, op_code, op_title, inputs=[2,2], outputs = [1]):
        self.op_code = op_code
        self.op_title = op_title

        super().__init__(scene, self.op_title, inputs, outputs)

    def initInnerClasses(self):
        CalcContent = self.getNodeContentClass()
        CalcGraphicsNode = self.getGraphicsNodeClass()

