from django.utils.translation import ugettext_lazy as _

from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo


###############################################################################
# OMNIDIA GENERAL

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


###############################################################################
# OMNIDIA FILES

class FileType(GraphObject):
    __primarykey__ = 'id'

    name = Property()
    files = RelatedFrom('File', 'HAS_TYPE')


class File(GraphObject):
    __primarykey__ = 'id'

    name = Property()
    path = Property()
    hash = Property()
    type = RelatedTo('FileType')


# OMNIDIA FILE FIELDS ------------------------------------

class _Field(GraphObject):
    __primarykey__ = 'id'

    name = Property()
    minimum = Property()
    maximum = Property()
    filetype = RelatedTo('FileType')


class Field(_Field):
    datatype = RelatedTo('DataType')


class DatasetField(_Field):
    dataset = RelatedTo('Dataset')


###############################################################################
# OMNIDIA MODELS

class Model(GraphObject):
    __primarykey__ = 'id'
