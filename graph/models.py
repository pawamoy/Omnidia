import hashlib
import os
import shutil

from django.conf import settings
from django.utils.text import slugify

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
    def all(cls, *labels):
        return cls.filter(*labels)

    @classmethod
    def filter(cls, *labels, **properties):
        selection = ns.select(cls.__name__, *labels, **properties)
        return [cls(n) for n in selection]

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
        return self['name']

    def save(self):
        g.push(self.node)

    def edges(self, rel_type=None, end_node=None, bidirectional=False, limit=None):
        return [Edge(r) for r in g.match(self.node, rel_type, end_node, bidirectional, limit)]

    def delete(self):
        for edge in self.edges(bidirectional=True):
            edge.delete()
        g.delete(self.node)


class Dataset(Node):
    EDGE_TYPE = 'VALUE_OF'

    @property
    def values(self):
        return [
            DatasetValue(list(walk(edge.relationship))[0])
            for edge in self.edges(Dataset.EDGE_TYPE, bidirectional=True)
        ]

    @property
    def text_values(self):
        return [v.name for v in self.values]

    def add_value(self, value):
        value = DatasetValue.get_or_create(name=value)
        edge = Edge.create(value.node, Dataset.EDGE_TYPE, self.node)
        return edge, value

    def separate_value(self, value):
        if isinstance(value, str):
            value = DatasetValue.get(name=value)
        for edge in self.edges(Dataset.EDGE_TYPE, value.node, bidirectional=True):
            edge.delete()


class DatasetValue(Node):
    pass


class File(Node):
    def _get_path(self):
        return self.node['path']

    def _set_path(self, value):
        self.node['path'] = value

    path = property(_get_path, _set_path)

    def _get_hash(self):
        return self.node['hash']

    def _set_hash(self, value):
        self.node['hash'] = value

    hash = property(_get_hash, _set_hash)

    @staticmethod
    def hash_file(f, hasher, block_size=65536):
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
        return hasher.hexdigest()

    @staticmethod
    def get_path_relative_to_media_root(path):
        path = path.split(settings.MEDIA_ROOT)[1]
        if path.startswith(os.sep):
            path = path[1:]
        return path

    @staticmethod
    def add(path):
        new_file = File.create(path=path)
        new_file.update_hash(save=False)
        new_file.rename_object(path.split(os.sep)[-1])

    def compute_hash(self):
        with open(self.path, 'rb') as f:
            return File.hash_file(f, hashlib.sha256())

    def update_hash(self, save=True):
        self.hash = self.compute_hash()
        if save:
            self.save()

    def set_path(self, path, save=True):
        if os.path.isabs(path):
            path = File.get_path_relative_to_media_root(path)
        self.path = path
        if save:
            self.save()

    def move(self, new_path):
        # Here we assume new_path is relative and inside MEDIA_ROOT,
        # because each file going out of MEDIA_ROOT is not watched anymore,
        # and we don't want that. We have to explicitly COPY the file somewhere
        # else and then DELETE it from the database and the MEDIA_ROOT.
        shutil.move(os.path.join(settings.MEDIA_ROOT, self.path),
                    os.path.join(settings.MEDIA_ROOT, new_path))
        self.set_path(new_path)

    def get_filename(self):
        return self.path.split(os.sep)[-1]

    def get_relative_path(self):
        return File.get_path_relative_to_media_root(self.path)

    def get_absolute_path(self):
        return self.path

    def rename_file(self, new_name):
        self.move(os.path.join(os.path.dirname(self.get_relative_path()), new_name))

    def rename_object(self, new_name, save=True):
        self.node['name'] = new_name
        if save:
            self.save()

    def apply_filename_from_object_name(self):
        self.rename_file(slugify(self.name))

    def apply_object_name_from_filename(self):
        self.rename_object(self.get_filename())
