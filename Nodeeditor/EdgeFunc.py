from Nodeeditor.GraphicalEdge import *

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_CURVE = 2

class AllEdgeFunctions(Serializable):
    def __init__(self, scene, start_socket=None, end_socket=None, edge_type=EDGE_TYPE_DIRECT):
        super().__init__()
        self.scene = scene

        self.new_start_socket = None
        self.new_end_socket = None

        self.start_socket = start_socket
        self.end_socket = end_socket
        self.edge_type = edge_type

        self.scene.addEdge(self)

# #to know the edge place in memory just in terminal
#     def __str__(self):
#         return "<Edge %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    @property
    def start_socket(self): return self.new_start_socket

    @start_socket.setter
    def start_socket(self, value):
        # if we were assigned to some socket before, delete us from the socket
        if self.new_start_socket is not None:
            self.new_start_socket.removeEdge(self)

        # assign new start socket
        self.new_start_socket = value
        # addEdge to the Socket class
        if self.start_socket is not None:
            self.start_socket.addEdge(self)

    @property
    def end_socket(self): return self.new_end_socket

    @end_socket.setter
    def end_socket(self, value):
        # if we were assigned to some socket before, delete us from the socket
        if self.new_end_socket is not None:
            self.new_end_socket.removeEdge(self)

        # assign new end socket
        self.new_end_socket= value
        # addEdge to the Socket class
        if self.end_socket is not None:
            self.end_socket.addEdge(self)

    @property
    def edge_type(self): return self.edge_type_chosen

    @edge_type.setter
    def edge_type(self, value):
        if hasattr(self, 'grEdge') and self.grEdge is not None:
            self.scene.grScene.removeItem(self.grEdge)

        self.edge_type_chosen = value

        if self.edge_type == EDGE_TYPE_DIRECT:
            self.grEdge = GraphicalEdgeDirect(self)
        elif self.edge_type == EDGE_TYPE_CURVE:
            self.grEdge = GraphicalEdgeCurve(self)
        else:
            self.grEdge = GraphicalEdgeCurve(self)

        self.scene.grScene.addItem(self.grEdge)
        if self.start_socket is not None:
            self.updatePositions()

    def updatePositions(self):
        start_pos = self.start_socket.getSocketPosition()
        start_pos[0] += self.start_socket.node.grNode.pos().x()
        start_pos[1] += self.start_socket.node.grNode.pos().y()
        self.grEdge.setSource(*start_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x()
            end_pos[1] += self.end_socket.node.grNode.pos().y()
            self.grEdge.setDestination(*end_pos)
        else:
            self.grEdge.setDestination(*start_pos)
        self.grEdge.update()

    def remove_from_sockets(self):
        self.end_socket = None
        self.start_socket = None

    def remove(self):
        self.remove_from_sockets()
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge = None
        try:
            self.scene.removeEdge(self)
        except ValueError:
            pass

    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('edge_type', self.edge_type),
            ('start', self.start_socket.id),
            ('end', self.end_socket.id),
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        if restore_id: self.id = data['id']
        self.start_socket = hashmap[data['start']]
        self.end_socket = hashmap[data['end']]
        self.edge_type = data['edge_type']