import hashlib
import os
import shutil

from django.conf import settings
from django.utils.text import slugify

from py2neo import Node as _Node, Relationship as _Edge, walk, Subgraph

from . import g, ns
from .exceptions import MultipleNodeError


def node_property(name):
    def get(self):
        return self.node[name]

    def set(self, value):
        self.node[name] = value

    return property(get, set)


class Edge(object):
    def __init__(self, edge):
        self.edge = edge

    @classmethod
    def create(cls, *args, **properties):
        edge = _Edge(*args, **properties)
        g.create(edge)
        return cls(edge)

    def start_node(self):
        return list(walk(self.edge))[0]

    def end_node(self):
        return list(walk(self))[-1]

    def delete(self):
        g.separate(self.edge)


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
        selection = ns.select(cls.__name__, *labels).order_by('_.name')
        return [cls(n) for n in selection]

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

    def _get_name(self):
        return self.node['name']

    def _set_name(self, value):
        self.node['name'] = value

    name = property(_get_name, _set_name)

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
            DatasetValue(list(walk(edge.edge))[0])
            for edge in self.edges(Dataset.EDGE_TYPE, bidirectional=True)
        ]

    @property
    def text_values(self):
        return [v.name for v in self.values]

    def add_value(self, value):
        value = DatasetValue.get_or_create(name=value)
        edge = Edge.create(value.node, Dataset.EDGE_TYPE, self.node)
        return edge, value

    def add_values(self, values):
        nodes = [_Node('DatasetValue', name=v) for v in values]
        g.create(Subgraph(nodes))
        edges = [_Edge(n, Dataset.EDGE_TYPE, self.node) for n in nodes]
        g.create(Subgraph(nodes, edges))

    def separate_value(self, value):
        if isinstance(value, str):
            value = DatasetValue.get(name=value)
        for edge in self.edges(Dataset.EDGE_TYPE, value.node, bidirectional=True):
            edge.delete()


class DatasetValue(Node):
    is_premium = node_property('is_premium')


class File(Node):
    HASHER = hashlib.sha256
    BLOCK_SIZE = 65536

    def _get_path(self):
        return self.node['path']

    def _set_path(self, value):
        self.node['path'] = value

    path = property(_get_path, _set_path)

    def _get_file_hash(self):
        return self.node['file_hash']

    def _set_file_hash(self, value):
        self.node['file_hash'] = value

    file_hash = property(_get_file_hash, _set_file_hash)

    def _get_path_hash(self):
        return self.node['path_hash']

    def _set_path_hash(self, value):
        self.node['path_hash'] = value

    path_hash = property(_get_path_hash, _set_path_hash)

    @staticmethod
    def hash_file(f, hasher=HASHER, block_size=BLOCK_SIZE):
        hasher = hasher()
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
        return hasher.hexdigest()

    @staticmethod
    def hash_path(path, hasher=HASHER):
        hash_object = hasher(path.encode('utf-8'))
        return hash_object.hexdigest()

    @staticmethod
    def get_path_relative_to_media_root(path):
        path = path.split(settings.MEDIA_ROOT)[1]
        if path.startswith(os.sep):
            path = path[1:]
        return path

    @staticmethod
    def add(path):
        new_file = File.create(path=path)
        new_file.update_hash()
        new_file.rename_node(path.split(os.sep)[-1])
        new_file.save()

    @staticmethod
    def in_path(path):
        re_startswith_path = '^%s%s.*' % (path, os.sep)
        selection = ns.select('File')
        matching_files = selection.where("_.path =~ '%s'" % re_startswith_path)
        return (File(n) for n in matching_files)

    def delete(self, from_disk=True):
        super().delete()
        if from_disk and os.path.exists(self.path):
            os.remove(self.path)

    def get_file_hash(self):
        if os.path.exists(self.path):
            with open(self.path, 'rb') as f:
                return File.hash_file(f)

    def get_path_hash(self):
        return File.hash_path(self.path)

    def update_hash(self):
        self.update_file_hash()
        self.update_path_hash()

    def update_file_hash(self):
        self.file_hash = self.get_file_hash()

    def update_path_hash(self):
        self.path_hash = self.get_path_hash()

    def set_path(self, path):
        if os.path.isabs(path):
            path = File.get_path_relative_to_media_root(path)
        self.path = path

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

    def rename_node(self, new_name):
        self.name = new_name

    def apply_filename_from_node_name(self):
        self.rename_file(slugify(self.name))

    def apply_node_name_from_filename(self):
        self.rename_node(self.get_filename())


class Object(Node):
    pass
