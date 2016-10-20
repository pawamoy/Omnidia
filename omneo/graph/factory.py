from django.utils.translation import ugettext_lazy as _

from . import g, ns
from .models import FileType, AbstractFile, ObjectType, AbstractObject


# Algorithm:

# For each file type, get the associated fields, build a class that inherits
# from AbstractFile, and set the fields as properties or relations.

# Do the same for objects.

# For each class, add methods to check limitations for fields.

def get_file_type_fields(file_type):
    return [file_type.fields]


def build_file_types():
    file_types = ns.select('FileType')
    for file_type in file_types:
        fields = get_file_type_fields(file_type)
