from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo


class Dataset(GraphObject):
    name = Property()
    values = RelatedFrom('DatasetValue', 'VALUE_OF')


class DatasetValue(GraphObject):
    value = Property()
    dataset = RelatedTo('Dataset')


class File(GraphObject):
    __primarykey__ = 'path'  # or hash?

    labels = ('File', )

    name = Property()
    path = Property()
    hash = Property()


class Object(GraphObject):
    __primarykey__ = 'id'

    labels = ('Object', )

    id = Property()
