from collections import OrderedDict
from Nodeeditor.SerializationFunc import Serializable
from PyQt5.QtWidgets import *


class AllContentWidgetFunctions(QWidget, Serializable):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)

        self.createContentWidget()

    def createContentWidget(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.widget_label = QLabel("\tSome Title")
        self.layout.addWidget(self.widget_label)
        self.layout.addWidget(TextSpaceEditing("Here Our Text"))

    def setEditingFlag(self, value):
        self.node.scene.grScene.views()[0].editingFlag = value

    def serialize(self):
        return OrderedDict([])

    def deserialize(self, data, hashmap={}):
        return False

########### ely katb el code da y5osh yktb howa by3ml eh 3shan nfhmo
class TextSpaceEditing(QTextEdit):
    def focusInEvent(self, event):
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.parentWidget().setEditingFlag(False)
        super().focusOutEvent(event)
