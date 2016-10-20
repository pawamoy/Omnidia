from django.utils.translation import ugettext_lazy as _

from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo


# General

class DataType(GraphObject):
    """The type of data stored in a particular field.

    The available types are hardcoded:

        text
        date
        datetime
        time
        integer
        float
        binary

    We could also add types like hexadecimal, octal, ...
    """

    TYPE_TEXT = 0
    TYPE_DATE = 1
    TYPE_DATETIME = 2
    TYPE_TIME = 3
    TYPE_INTEGER = 4
    TYPE_FLOAT = 5
    TYPE_BINARY = 6

    TYPES = (
        [TYPE_TEXT, _('Text')],
        [TYPE_DATE, _('Date')],
        [TYPE_DATETIME, _('Datetime')],
        [TYPE_TIME, _('Time')],
        [TYPE_INTEGER, _('Integer')],
        [TYPE_FLOAT, _('Float')],
        [TYPE_BINARY, _('Binary')],
    )


class Dataset(GraphObject):
    __primarykey__ = 'id'

    name = Property()
    type = RelatedTo('DataType')
    values = RelatedFrom('DatasetValue', 'VALUE_OF')


class DatasetValue(GraphObject):
    __primarykey__ = 'id'

    value = Property()
    dataset = RelatedTo('Dataset')


# Files

class FileType(GraphObject):
    __primarykey__ = 'id'

    name = Property()


class AbstractFile(GraphObject):
    __primarykey__ = 'id'

    name = Property()
    path = Property()
    hash = Property()


class FileField(GraphObject):
    __primarykey__ = 'id'

    name = Property()
    minimum = Property()
    maximum = Property()
    file_type = RelatedTo('FileType')


class FileDataField(FileField):
    data_type = RelatedTo('DataType')


class FileDatasetField(FileField):
    dataset = RelatedTo('Dataset')


# Objects

class ObjectType(GraphObject):
    __primarykey__ = 'id'

    name = Property()


class AbstractObject(GraphObject):
    __primarykey__ = 'id'


class ObjectField(GraphObject):
    __primarykey__ = 'id'

    name = Property()
    minimum = Property()
    maximum = Property()
    object_type = RelatedTo('ObjectType')


class ObjectDataField(ObjectField):
    data_type = RelatedTo('DataType')


class ObjectDatasetField(ObjectField):
    dataset = RelatedTo('Dataset')


class ObjectToObjectField(ObjectField):
    to_object = RelatedTo('ObjectType')
