from py2neo import Node as _Node, Relationship, walk

from . import g, ns
from .exceptions import MultipleNodeError


class Edge(object):
    def __init__(self, relationship):
        self.relationship = relationship

    @classmethod
    def create(cls, *args, **properties):
        relationship = Relationship(*args, **properties)
        g.create(relationship)
        return cls(relationship)

    def start_node(self):
        return list(walk(self.relationship))[0]

    def end_node(self):
        return list(walk(self))[-1]

    def delete(self):
        g.separate(self.relationship)


class Node(object):
    def __init__(self, node):
        self.node = node

    def __eq__(self, other):
        return self.name == other.name and self.node == other.node

    @classmethod
    def create(cls, *labels, **properties):
        node = _Node(cls.__name__, *labels, **properties)
        g.create(node)
        return cls(node)

    @classmethod
    def all(cls, label=None):
        if label is None:
            label = cls.__name__
        return (cls(node) for node in g.find(label))

    @classmethod
    def filter(cls, *labels, **properties):
        return [cls(n) for n in ns.select(cls.__name__, *labels, **properties)]

    @classmethod
    def get(cls, *labels, **properties):
        nodes = cls.filter(*labels, **properties)
        if nodes:
            if len(nodes) == 1:
                return nodes[0]
            raise MultipleNodeError('%s.get returned %d nodes matching "%s"' % (
                cls.__name__, len(nodes), properties))
        return None

    @classmethod
    def get_or_create(cls, *labels, **properties):
        node = cls.get(*labels, **properties)
        if node:
            return node
        node = cls.create(*labels, **properties)
        return node

    @property
    def labels(self):
        return [l for l in self.node.labels()]

    @property
    def properties(self):
        return dict(self.node)

    @property
    def name(self):
        return self.properties['name']

    def save(self):
        g.push(self.node)

    def edges(self, rel_type=None, end_node=None, bidirectional=False, limit=None):
        return [Edge(r) for r in g.match(self.node, rel_type, end_node, bidirectional, limit)]

    def delete(self):
        for edge in self.edges(bidirectional=True):
            edge.delete()
        g.delete(self.node)


class Dataset(Node):
    @property
    def values(self):
        return [
            DatasetValue(list(walk(edge.relationship))[0])
            for edge in self.edges('VALUE_OF', bidirectional=True)
        ]

    @property
    def text_values(self):
        return [v.name for v in self.values]

    def add_value(self, value):
        value = DatasetValue.get_or_create(name=value)
        edge = Edge.create(value.node, 'VALUE_OF', self.node)
        return edge, value

    def separate_value(self, value):
        if isinstance(value, str):
            value = DatasetValue.get(value)
        edges = [Edge(r) for r in g.match(self.node, 'VALUE_OF', value.node, bidirectional=True)]
        for edge in edges:
            edge.delete()


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
