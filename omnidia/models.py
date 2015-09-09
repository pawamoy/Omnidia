import hashlib
import shutil
import os
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from core.settings import MEDIA_ROOT
from omnidia.utils import hashfile
# TODO: set model methods
# FIXME: all max_length=30 to 255 ?

# NOTE: these models could be used in a django app called django-dcarve,
# django-carved or django-dynamic-carve for
# Django Dynamic Class Attribute and Relational Value Entity.
# The letters are mixed up, it should be
# Django Dynamic Entity Attribute Value with Classes and Relations
# but it would give django-deavcr which is unpronounceable.

###############################################################################
# OMNIDIA GENERAL

class DataType(object):
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


class Dataset(models.Model):
    """A dataset is an array of static values. Each value of the same dataset
    has the same type.
    """

    name = models.CharField(_('Name'), max_length=30)
    datatype = models.PositiveSmallIntegerField(
        choices=DataType.TYPES, verbose_name=_('Data type'))

    class Meta:
        verbose_name = _('Dataset')
        verbose_name_plural = _('Datasets')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Dataset(%r, %r)' % (self.name, self.datatype)

    @staticmethod
    def new(name, datatype):
        """Create a new Dataset instance, and return it.

        :param name: str, the dataset name
        :param datatype: integer, see :class:`DataType`,
            the data type of the dataset
        :return: :class:`Dataset`, model instance
        """

        return Dataset.objects.create(name=name, datatype=datatype)

    def add(self, value):
        """Add a value into a Dataset instance.

        :param value: str, the value to add
        """

        DatasetValue.objects.create(dataset=self, value=value)

    def get(self, value):
        """Try to return the DatasetValue instance with specified value.

        :param value: str, the value you are searching for
        :return: :class:`DatasetValue`, model instance
        """

        try:
            return DatasetValue.objects.get(dataset=self, value=value)
        except DatasetValue.DoesNotExist:
            return None

    def remove(self, value):
        """Try to remove the dataset value with specified value.

        :param value: str, the value to remove from the dataset
        :return: bool, True if removed correctly, else False
        """

        dv = self.get(value)
        return True if dv and dv.delete() else False


class DatasetValue(models.Model):
    """The values contained in datasets. Each value is stored as text,
    with a maximum length of 255 characters.
    """

    value = models.CharField(_('Value'), max_length=255)
    dataset = models.ForeignKey(Dataset,
                                verbose_name=_('Dataset'),
                                related_name='values')

    class Meta:
        verbose_name = _('Dataset value')
        verbose_name_plural = _('Dataset values')
        unique_together = ('dataset', 'value')

    def __str__(self):
        return self.value

    def __repr__(self):
        return 'DatasetValue(%r, %r)' % (self.dataset, self.value)


###############################################################################
# OMNIDIA FILES

class FileType(models.Model):
    """The available types for files. Each file type can have specific
    attributes (through FileField models).
    """

    name = models.CharField(_('File type'), max_length=30)

    class Meta:
        verbose_name = _('File type')
        verbose_name_plural = _('File types')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'FileType(%r)' % self.name

    @staticmethod
    def new(name):
        """Create a new FileType instance, and return it.

        :param name: str, the name of the file type
        :return: :class:`Dataset`, model instance
        """

        return FileType.objects.create(name=name)


class File(models.Model):
    """The File model represents file that are tracked by Omnidia.

    It stores the hash of the file, which is recomputed each time the file
    is modified, and can be used to find files that are not tracked by
    Omnidia, by comparing their respective hash.
    """

    name = models.CharField(
        _('Filename'), max_length=255,
        help_text=_('The new name to use for searching in the database. '
                    'Leave empty to use the current name.'))
    file = models.FileField(_('File location'), upload_to='%Y/%m/%d')
    hash = models.CharField(_('SHA256 hash'), max_length=256)
    type = models.ForeignKey(FileType,
                             verbose_name=_('File type'),
                             related_name='files')

    class Meta:
        # FIXME: with two identical files: same hash, what to do?
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'File(%r, %r, %r, %r)' % (self.name, self.file,
                                         self.type, self.hash)

    @staticmethod
    def add(file_path):
        # create the object
        # give it a type based on ext or mimetype
        # compute its hash
        # give it a name based on its path
        pass

    @staticmethod
    def get(path):
        """Try to return a File instance based on given path.

        :param path: str, the absolute path of the file
        :return: :class:`File`, model instance or None
        """
        try:
            return File.objects.get(file=path)
        except File.DoesNotExist:
            return None

    get_by_path = get

    @staticmethod
    def get_by_hash(h):
        """Try to return a File instance based on given hash.

        :param hash: str, the SHA256 hash of the file
        :return: :class:`File`, model instance or None
        """
        try:
            return File.objects.get(hash=h)
        except File.DoesNotExist:
            return None

    def compute_hash(self):
        """Recompute the hash of the file.

        :return: str, the refreshed hash
        """
        with self.file.open('rb') as f:
            return hashfile(f, hashlib.sha256())

    # def move(self, new_path):
    #     if os.path.exists(os.path.dirname(new_path)):

    @staticmethod
    def get_path_relative_to_media_root(path):
        path = path.split(MEDIA_ROOT)[1]
        if path.startswith(os.sep):
            path = path[1:]
        return path

    def set_path(self, path):
        if os.path.isabs(path):
            path = File.get_path_relative_to_media_root(path)
        self.file.name = path
        self.save()

    def move(self, new_path):
        # Here we assume new_path is relative and inside MEDIA_ROOT,
        # because each file going out of MEDIA_ROOT is not watched anymore,
        # and we don't want that. We have to explicitly COPY the file somewhere
        # else and then DELETE it from the database and the MEDIA_ROOT.
        shutil.move(os.path.join(MEDIA_ROOT, self.file),
                    os.path.join(MEDIA_ROOT, new_path))
        self.set_path(new_path)

    def get_filename(self):
        return self.file.name.split(os.sep)[-1]

    def get_relative_path(self):
        return File.get_path_relative_to_media_root(self.file.path)

    def get_absolute_path(self):
        return self.file.path

    def rename_file(self, new_name):
        self.move(os.path.join(os.path.dirname(self.get_relative_path()),
                               new_name))

    def rename_object(self, new_name):
        self.name = new_name
        self.save()

    def apply_filename_from_object_name(self):
        self.rename_file(slugify(self.name))

    def apply_object_name_from_filename(self):
        self.rename_object(self.get_filename())

    # def remove(self, from_database=False):



    # TODO: method to delete, copy, archive, download, read, open


###############################################################################
# OMNIDIA FILE FIELDS

class FileGenericField(models.Model):
    """The abstract file field model. Each file field has a name, a minimum
    and a maximum value that defaults to 0 (which means unlimited).
    """

    name = models.CharField(_('Field name'), max_length=30)
    minimum = models.PositiveSmallIntegerField(
        _('Minimum'), default=0,
        help_text=_('Set to 0 to make this field optional'))
    maximum = models.PositiveSmallIntegerField(
        _('Maximum'), default=0,
        help_text=_('Set to 0 to have no limitation'))

    class Meta:
        verbose_name = _('File generic field')
        verbose_name_plural = _('File generic fields')
        abstract = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'FileGenericField(%r, %r, %r)' % (
            self.name, self.minimum, self.maximum)


class FileDatasetField(FileGenericField):
    """A field to store a dataset value for a particular file type.
    """

    dataset = models.ForeignKey(Dataset,
                                verbose_name=_('Dataset'),
                                related_name='file_fields')
    filetype = models.ForeignKey(FileType,
                                 verbose_name=_('File type'),
                                 related_name='dataset_fields')

    class Meta:
        verbose_name = _('File dataset field')
        verbose_name_plural = _('File dataset fields')
        unique_together = ('filetype', 'name')

    def __repr__(self):
        return 'FileDatasetField(%r, %r, %r, %r, %r)' % (
            self.name, self.minimum, self.maximum, self.dataset, self.filetype)


class FileSpecificField(FileGenericField):
    """A field to store a value of a certain type for a particular file type.
    """

    filetype = models.ForeignKey(FileType,
                                 verbose_name=_('File type'),
                                 related_name='specific_fields')
    datatype = models.PositiveSmallIntegerField(
        choices=DataType.TYPES, verbose_name=_('Data type'))

    class Meta:
        verbose_name = _('File specific field')
        verbose_name_plural = _('File specific fields')
        unique_together = ('filetype', 'name')

    def __repr__(self):
        return 'FileSpecificField(%r, %r, %r, %r, %r)' % (
            self.name, self.minimum, self.maximum,
            self.filetype, self.datatype)


class FileGlobalField(FileGenericField):
    """A field to store a value of a certain type for all file types.
    """

    datatype = models.PositiveSmallIntegerField(
        choices=DataType.TYPES, verbose_name=_('Data type'))

    class Meta:
        verbose_name = _('File global field')
        verbose_name_plural = _('File global fields')

    def __repr__(self):
        return 'FileGlobalField(%r, %r, %r, %r)' % (
            self.name, self.minimum, self.maximum, self.dataype)


class FileGlobalDatasetField(FileGenericField):
    """A field to store dataset values for all file types.
    """

    dataset = models.ForeignKey(Dataset,
                                verbose_name=_('Datasets'),
                                related_name='file_global_fields')

    class Meta:
        verbose_name = _('File global dataset field')
        verbose_name_plural = _('File global dataset fields')

    def __repr__(self):
        return 'FileGlobalDatasetField(%r, %r)' % (self.file, self.dataset)


###############################################################################
# OMNIDIA FILE VALUES

class FileGenericValue(models.Model):
    """The abstract field value model. The value is always attached to a
    specific file (File model).
    """

    file = models.ForeignKey(File, verbose_name=_('File'), related_name='+')

    class Meta:
        verbose_name = _('File generic value')
        verbose_name_plural = _('File generic values')
        abstract = True

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return 'FileGenericValue(%r)' % self.file


class FileDatasetValue(FileGenericValue):
    """The values of dataset fields.
    """

    field = models.ForeignKey(FileDatasetField,
                              verbose_name=_('Field'),
                              related_name='values')
    value = models.ForeignKey(DatasetValue,
                              verbose_name=_('Value'),
                              related_name='file_values')

    class Meta:
        verbose_name = _('File dataset value')
        verbose_name_plural = _('File dataset values')

    def __repr__(self):
        return 'FileDatasetField(%r, %r)' % (self.file, self.value)


class FileSpecificValue(FileGenericValue):
    """The values of specific fields.
    """

    value = models.TextField(_('Value'))
    field = models.ForeignKey(FileSpecificField,
                              verbose_name=_('Field'),
                              related_name='values')

    class Meta:
        verbose_name = _('File specific value')
        verbose_name_plural = _('File specific values')

    def __repr__(self):
        return 'FileSpecificField(%r, %r, %r)' % (
            self.file, self.field, self.value)


class FileGlobalValue(FileGenericValue):
    """The values of global fields.
    """

    value = models.TextField(_('Value'))
    field = models.ForeignKey(FileGlobalField,
                              verbose_name=_('Field'),
                              related_name='values')

    class Meta:
        verbose_name = _('File global value')
        verbose_name_plural = _('File global values')

    def __repr__(self):
        return 'FileGlobalField(%r, %r, %r)' % (
            self.file, self.field, self.value)


class FileGlobalDatasetValue(FileGenericValue):
    """The values of global dataset fields.
    """

    field = models.ForeignKey(FileGlobalDatasetField,
                              verbose_name=_('Field'),
                              related_name='values')
    value = models.ForeignKey(DatasetValue,
                              verbose_name=_('Value'),
                              related_name='file_global_values')

    class Meta:
        verbose_name = _('File global dataset value')
        verbose_name_plural = _('File global dataset values')

    def __repr__(self):
        return 'FileGlobalDatasetValue(%r, %r)' % (self.file, self.value)


###############################################################################
# OMNIDIA MODELS

class Model(models.Model):
    """Model instances are entities that define the properties of objects.
    A Model instance is constructed with a name, then you can add fields to it,
    through the ModelField models.
    """

    name = models.CharField(_('Name'), max_length=30)

    class Meta:
        verbose_name = _('Model')
        verbose_name_plural = _('Models')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Model(%r)' % self.name


class Object(models.Model):
    """An Object instance is an instance of a some Model. It is an object
    composed of the Model fields as values. Each object is attached to a
    specific Model in order to know which information to search for.
    """

    name = models.CharField(_('Name'), max_length=255)
    model = models.ForeignKey(Model,
                              verbose_name=_('Model'),
                              related_name='object_set')

    class Meta:
        verbose_name = _('Object')
        verbose_name_plural = _('Objects')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Object(%r, %r)' % (self.name, self.model)


class ObjectLink(models.Model):
    """Minimalist links between objects. Use the LinkData model to add
    information on links.
    """

    help_text = _('Order matters. It is like an arrow pointing on B from A.')
    object_ref1 = models.ForeignKey(Object,
                                    verbose_name=_('Object A'),
                                    related_name='links_to',
                                    help_text=help_text)
    object_ref2 = models.ForeignKey(Object,
                                    verbose_name=_('Object B'),
                                    related_name='links_from',
                                    help_text=help_text)

    class Meta:
        verbose_name = _('Object link')
        verbose_name_plural = _('Object links')
        unique_together = ('object_ref1', 'object_ref2')

    def __str__(self):
        return '%s - %s' % (self.object_ref1, self.object_ref2)

    def __repr__(self):
        return 'ObjectLink(%r, %r)' % (self.object_ref1, self.object_ref2)


class LinkData(models.Model):
    """Information about links between objects.
    """

    link = models.ForeignKey(ObjectLink,
                             verbose_name=_('Link'),
                             related_name='data')
    # TODO: add fields here

    class Meta:
        verbose_name = _('Link data')
        verbose_name_plural = _('Link data')

    def __str__(self):
        return str(self.link)

    def __repr__(self):
        return 'LinkData(%r)' % self.link


class ObjectFile(models.Model):
    """Association between an object and files. It is the way to attach
    files to abstract objects.
    """

    object = models.ForeignKey(Object,
                               verbose_name=_('Object'),
                               related_name='files')
    file = models.ForeignKey(File,
                             verbose_name=_('File'),
                             related_name='object_set')

    class Meta:
        verbose_name = _('Object file')
        verbose_name_plural = _('Object files')
        unique_together = ('object', 'file')

    def __str__(self):
        return '%s - %s' % (self.object, self.file)

    def __repr__(self):
        return 'ObjectFile(%r, %r)' % (self.object, self.file)


###############################################################################
# OMNIDIA MODEL FIELDS

class ModelGenericField(models.Model):
    """The abstract model field model. Each model field has a name,
    a minimum and a maximum value that defaults to 0 (which means unlimited).
    """

    name = models.CharField(_('Name'), max_length=30)
    minimum = models.PositiveSmallIntegerField(
        _('Minimum'), default=0,
        help_text=_('Set to 0 to make this field optional'))
    maximum = models.PositiveSmallIntegerField(
        _('Maximum'), default=0,
        help_text=_('Set to 0 to have no limitation'))

    class Meta:
        verbose_name = _('Model generic field')
        verbose_name_plural = _('Model generic fields')
        abstract = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'ModelGenericField(%r, %r, %r)' % (
            self.name, self.minimum, self.maximum)


class ModelDatasetField(ModelGenericField):
    """A field to store a dataset value for a particular model.
    """

    dataset = models.ForeignKey(Dataset,
                                verbose_name=_('Dataset'),
                                related_name='model_fields')
    model = models.ForeignKey(Model,
                              verbose_name=_('Model'),
                              related_name='dataset_fields')

    class Meta:
        verbose_name = _('Model dataset field')
        verbose_name_plural = _('Model dataset fields')
        unique_together = ('model', 'name')

    def __repr__(self):
        return 'ModelDatasetField(%r, %r, %r, %r, %r)' % (
            self.name, self.minimum, self.maximum, self.dataset, self.model)


class ModelSpecificField(ModelGenericField):
    """A field to store a value of a certain type for a particular model.
    """

    model = models.ForeignKey(Model,
                              verbose_name=_('Model'),
                              related_name='specific_fields')
    datatype = models.PositiveSmallIntegerField(
        choices=DataType.TYPES, verbose_name=_('Data type'))

    class Meta:
        verbose_name = _('Model specific field')
        verbose_name_plural = _('Model specific fields')
        unique_together = ('model', 'name')

    def __repr__(self):
        return 'ModelSpecificField(%r, %r, %r, %r, %r)' % (
            self.name, self.minimum, self.maximum, self.model, self.datatype)


class ModelGlobalField(ModelGenericField):
    """A field to store a value of a certain type for all models.
    """

    datatype = models.PositiveSmallIntegerField(
        choices=DataType.TYPES, verbose_name=_('Data type'))

    class Meta:
        verbose_name = _('Model global field')
        verbose_name_plural = _('Model global fields')

    def __repr__(self):
        return 'ModelGlobalField(%r, %r, %r, %r)' % (
            self.name, self.minimum, self.maximum, self.datatype)


class ModelGlobalDatasetField(ModelGenericField):
    """A field to store a dataset value for all models.
    """

    dataset = models.ForeignKey(Dataset,
                                verbose_name=_('Dataset'),
                                related_name='model_global_fields')

    class Meta:
        verbose_name = _('Model global dataset field')
        verbose_name_plural = _('Model global dataset fields')

    def __repr__(self):
        return 'ModelGlobalDatasetField(%r, %r, %r, %r)' % (
            self.name, self.minimum, self.maximum, self.dataset)


class ModelModelField(ModelGenericField):
    """A field to store the reference to another model for a particular model.
    """

    source = models.ForeignKey(Model,
                               verbose_name=_('Source'),
                               related_name='include',
                               help_text=_('Source model'))
    target = models.ForeignKey(Model,
                               verbose_name=_('Target'),
                               related_name='included_in',
                               help_text=_('Targeted model'))

    class Meta:
        verbose_name = _('Model to-model field')
        verbose_name_plural = _('Model to-model fields')
        unique_together = ('source', 'name')

    def __repr__(self):
        return 'ModelModelField(%r, %r, %r, %r, %r)' % (
            self.name, self.minimum, self.maximum, self.source, self.target)


###############################################################################
# OMNIDIA MODEL VALUES

class ModelGenericValue(models.Model):
    """The abstract field value model. The value is always attached to a
    specific object (Object model).
    """

    object = models.ForeignKey(Object,
                               verbose_name=_('Object'),
                               related_name='+')

    class Meta:
        verbose_name = _('Model generic value')
        verbose_name_plural = _('Model generic values')
        abstract = True

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return 'ModelGenericValue(%r)' % self.object


class ModelDatasetValue(ModelGenericValue):
    """The values of dataset fields.
    """

    field = models.ForeignKey(ModelDatasetField,
                              verbose_name=_('Field'),
                              related_name='values')
    value = models.ForeignKey(DatasetValue,
                              verbose_name=_('Value'),
                              related_name='model_values')

    class Meta:
        verbose_name = _('Model dataset value')
        verbose_name_plural = _('Model dataset values')

    def __repr__(self):
        return 'ModelDatasetValue(%r, %r, %r)' % (
            self.object, self.field, self.value)


class ModelSpecificValue(ModelGenericValue):
    """The values of specific fields.
    """

    field = models.ForeignKey(ModelSpecificField,
                              verbose_name=_('Field'),
                              related_name='values')
    value = models.TextField(_('Value'))

    class Meta:
        verbose_name = _('Model specific value')
        verbose_name_plural = _('Model specific values')

    def __repr__(self):
        return 'ModelSpecificValue(%r, %r, %r)' % (
            self.object, self.field, self.value)


class ModelGlobalValue(ModelGenericValue):
    """The values of global fields.
    """

    value = models.TextField(_('Value'))
    field = models.ForeignKey(ModelGlobalField,
                              verbose_name=_('Field'),
                              related_name='values')

    class Meta:
        verbose_name = _('Model global value')
        verbose_name_plural = _('Model global values')

    def __repr__(self):
        return 'ModelGlobalValue(%r, %r, %r)' % (
            self.object, self.field, self.value)


class ModelGlobalDatasetValue(ModelGenericValue):
    """The values of global dataset fields.
    """

    field = models.ForeignKey(ModelGlobalDatasetField,
                              verbose_name=_('Field'),
                              related_name='values')
    value = models.ForeignKey(DatasetValue,
                              verbose_name=_('Value'),
                              related_name='model_global_values')

    class Meta:
        verbose_name = _('Model global dataset value')
        verbose_name_plural = _('Model global dataset values')

    def __repr__(self):
        return 'ModelGlobalDatasetValue(%r, %r, %r)' % (
            self.object, self.field, self.value)


class ModelModelValue(ModelGenericValue):
    """The values of model-to-model fields.
    """

    field = models.ForeignKey(ModelModelField,
                              verbose_name=_('Field'),
                              related_name='values')
    value = models.ForeignKey(Object,
                              verbose_name=_('Value'),
                              related_name='value_of')

    class Meta:
        verbose_name = _('Model to-model value')
        verbose_name_plural = _('Model to-model values')

    def __repr__(self):
        return 'ModelModelValue(%r, %r, %r)' % (
            self.object, self.field, self.value)
