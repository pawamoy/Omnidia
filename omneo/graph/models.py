from py2neo import Node as _Node, Relationship, walk

from . import g
from .exceptions import MultipleNodeError


class Edge(object):
    def __init__(self, relationship):
        self.relationship = relationship

    def start_node(self):
        return list(walk(self.relationship))[0]

    def end_node(self):
        return list(walk(self))[-1]

    def delete(self):
        g.separate(self.relationship)

    @classmethod
    def create(cls, *args, **properties):
        relationship = Relationship(*args, **properties)
        g.create(relationship)
        return cls(relationship)


class Node(object):
    def __init__(self, node):
        self.node = node

    @classmethod
    def get(cls, name, limit=None):
        nodes = list(g.find(cls.__name__, 'name', name, limit))
        if nodes:
            if len(nodes) == 1:
                return cls(nodes[0])
            raise MultipleNodeError
        return None

    @classmethod
    def create(cls, *labels, **properties):
        node = _Node(cls.__name__, *labels, **properties)
        g.create(node)
        return cls(node)

    def save(self):
        g.push(self.node)

    @classmethod
    def all(cls, label=None):
        if label is None:
            label = cls.__name__
        return (cls(node) for node in g.find(label))

    def edges(self, rel_type=None, end_node=None, bidirectional=False, limit=None):
        return [Edge(r) for r in g.match(self.node, rel_type, end_node, bidirectional, limit)]

    @property
    def labels(self):
        return [l for l in self.node.labels()]

    @property
    def properties(self):
        return dict(self.node)

    def delete(self):
        for edge in self.edges(bidirectional=True):
            edge.delete()
        g.delete(self.node)

    @property
    def name(self):
        return self.properties['name']


class Dataset(Node):
    @property
    def values(self):
        return [
            dict(list(walk(edge.relationship))[0]).get('name')
            for edge in self.edges('VALUE_OF', bidirectional=True)
        ]

    def add_value(self, value):
        dv = DatasetValue.create(name=value)
        vo = Edge.create(dv.node, 'VALUE_OF', self.node)
        return vo, dv


class DatasetValue(Node):
    pass

# class File(GraphObject):
#     __primarykey__ = 'path'  # or hash?
#
#     labels = ('File', )
#
#     name = Property()
#     path = Property()
#     hash = Property()
