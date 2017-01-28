import hashlib

from django.db import models

from django_neomodel import DjangoNode, DjangoField
from neomodel import (
    RelationshipFrom, RelationshipTo, StructuredNode, StructuredRel, StringProperty,
    DateProperty, UniqueIdProperty, ZeroOrMore, OneOrMore, Relationship)


class Dataset(DjangoNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    values = RelationshipTo('DatasetValue', 'HAS_VALUE')

    class Meta:
        app_label = 'neograph'


class DatasetValue(DjangoNode):
    uid = UniqueIdProperty()
    dataset = RelationshipFrom('Dataset', 'HAS_VALUE', cardinality=OneOrMore)


class File(DjangoNode):
    HASHER = hashlib.sha256
    BLOCK_SIZE = 65536
    path = StringProperty(unique_index=True, required=True)
    path_hash = StringProperty(unique_index=True, required=True)
    file_hash = StringProperty(required=True)
    files = Relationship('File', 'FTF')
    objects = Relationship('Object', 'FTO')


class Object(DjangoNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    files = Relationship('File', 'OTF')
    objects = Relationship('Object', 'OTO')
