import json
from collections import OrderedDict
from Nodeeditor.SerializationFunc import Serializable
from Nodeeditor.GraphicalScene import DrawGraphicalScene
from Nodeeditor.NodeFunc import AllNodeFunctions
from Nodeeditor.EdgeFunc import AllEdgeFunctions
from Nodeeditor.SceneHistoryFunc import SceneHistory
from Nodeeditor.SceneClipboardFunc import AllSceneClipboardFunctions


class AllSceneFunctions(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []

        self.scene_width = 64000
        self.scene_height = 64000

        self._has_been_modified = False
        self._has_been_modified_listeners = []

        self.createScene()
        self.history = SceneHistory(self)
        self.clipboard = AllSceneClipboardFunctions(self)

    @property
    def has_been_modified(self):
        return False
        return self._has_been_modified

    @has_been_modified.setter
    def has_been_modified(self, value):
        if not self._has_been_modified and value:
            self._has_been_modified = value

            # call all registered listeners
            for callback in self._has_been_modified_listeners:
                callback()

        self._has_been_modified = value


    def addHasBeenModifiedListener(self, callback):
        self._has_been_modified_listeners.append(callback)

    def createScene(self):
        self.grScene = DrawGraphicalScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)


    def removeNode(self, node):
        if node in self.nodes:
            self.nodes.remove(node)

    def removeEdge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)

    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()

        self.has_been_modified = False


    def saveToFile(self, filename):
        with open(filename + ".json", "w") as file:
            file.write( json.dumps( self.serialize(), indent=4 ) )
            print("saving to", filename, "was successfull.")
            self.has_been_modified = False

    def loadFromFile(self, filename):
        with open(filename, "r") as file:
            raw_data = file.read()
            data = json.loads(raw_data)
            self.deserialize(data)
            self.has_been_modified = False


    def serialize(self):
        nodes, edges = [], []
        for node in self.nodes: nodes.append(node.serialize())
        for edge in self.edges: edges.append(edge.serialize())
        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.scene_width),
            ('scene_height', self.scene_height),
            ('nodes', nodes),
            ('edges', edges),
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        self.clear()
        hashmap = {}

        if restore_id: self.id = data['id']

        # create nodes
        for node_data in data['nodes']:
            AllNodeFunctions(self).deserialize(node_data, hashmap, restore_id)

        # create edges
        for edge_data in data['edges']:
            AllEdgeFunctions(self).deserialize(edge_data, hashmap, restore_id)

        return True