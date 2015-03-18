from django.db import models
from django.utils.translation import ugettext_lazy as _
# TODO: set help_text and other methods
# TODO: set docstrings
# TODO: add FileGlobalDatasetField ?


###############################################################################
# OMNIDIA GENERAL

class DataType(models.Model):
    """The type of data stored in a particular field.

    The available types are hardcoded:

        text
        date
        datetime
        time
        interger
        float
        binary

    We could also add types like hexadecimal, octal, ...
    """

    DATATYPE_CHOICES = (
        ['text', _('Text')],
        ['date', _('Date')],
        ['datetime', _('Datetime')],
        ['time', _('Time')],
        ['integer', _('Integer')],
        ['float', _('Float')],
        ['binary', _('Binary')],
    )
    name = models.CharField(_('Name'), max_length=30, choices=DATATYPE_CHOICES)

    class Meta:
        verbose_name = _('Data type')
        verbose_name_plural = _('Data types')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'DataType(%r)' % self.name


class Dataset(models.Model):
    """A dataset is an array of static values. Each value of the same dataset
    has the same type.
    """

    name = models.CharField(_('Name'), max_length=30)
    datatype = models.ForeignKey(DataType,
                                 verbose_name=_('Data type'),
                                 related_name='datasets')

    class Meta:
        verbose_name = _('Dataset')
        verbose_name_plural = _('Datasets')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Dataset(%r, %r)' % (self.name, self.datatype)


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


class File(models.Model):
    """The File model represents file that are tracked by Omnidia.

    It stores the hash of the file, which is recomputed each time the file
    is modified, and can be used to find files that are not tracked by
    Omnidia, by comparing their respective hash.
    """

    name = models.CharField(_('Filename'), max_length=255)
    # TODO: FileField or FilePathField ?
    file = models.FileField(_('File location'))
    hash = models.CharField(_('SHA256 Hash'), max_length=256)
    type = models.ForeignKey(FileType,
                             verbose_name=_('File type'),
                             related_name='files')

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'File(%r, %r, %r, %r)' % (self.name, self.file,
                                         self.type, self.hash)


###############################################################################
# OMNIDIA FILE FIELDS

class FileGenericField(models.Model):
    """The abstract file field model. Each file field has a name, minimum
    and maximum value that defaults to 0.
    """

    name = models.CharField(_('Field name'), max_length=30)
    minimum = models.PositiveSmallIntegerField(_('Minimum'), default=0)
    maximum = models.PositiveSmallIntegerField(_('Maximum'), default=0)

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
    datatype = models.ForeignKey(DataType,
                                 verbose_name=_('Data type'),
                                 related_name='file_specific_fields')

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

    datatype = models.ForeignKey(DataType,
                                 verbose_name=_('Data type'),
                                 related_name='file_global_fields')

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

    # TODO: add key to field
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

    # TODO: add key to field
    value = models.ForeignKey(DatasetValue,
                              verbose_name=_('Value'),
                              related_name='file_values')

    class Meta:
        verbose_name = _('File global dataset value')
        verbose_name_plural = _('File global dataset values')

    def __repr__(self):
        return 'FileGlobalDatasetValue(%r, %r)' % (self.file, self.value)


###############################################################################
# OMNIDIA MODELS

class Model(models.Model):
    name = models.CharField(_('Name'), max_length=30)

    class Meta:
        verbose_name = _('Model')
        verbose_name_plural = _('Models')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Model(%r)' % self.name


class Object(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    model = models.ForeignKey(Model,
                              verbose_name=_('Model'),
                              related_name='objects')

    class Meta:
        verbose_name = _('Object')
        verbose_name_plural = _('Objects')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Object(%r, %r)' % (self.name, self.model)


class ObjectLink(models.Model):
    object_ref1 = models.ForeignKey(Object,
                                    verbose_name=_('Object A'),
                                    related_name='links_to')
    object_ref2 = models.ForeignKey(Object,
                                    verbose_name=_('Object B'),
                                    related_name='links_from')

    class Meta:
        verbose_name = _('Object link')
        verbose_name_plural = _('Object links')
        unique_together = ('object_ref1', 'object_ref2')

    def __str__(self):
        return '%s - %s' % (self.object_ref1, self.object_ref2)

    def __repr__(self):
        return 'ObjectLink(%r, %r)' % (self.object_ref1, self.object_ref2)


class LinkData(models.Model):
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
    object = models.ForeignKey(Object,
                               verbose_name=_('Object'),
                               related_name='files')
    file = models.ForeignKey(File,
                             verbose_name=_('File'),
                             related_name='objects')

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
    name = models.CharField(_('Name'), max_length=30)
    minimum = models.PositiveSmallIntegerField(_('Minimum'), default=0)
    maximum = models.PositiveSmallIntegerField(_('Maximum'), default=0)

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
    model = models.ForeignKey(Model,
                              verbose_name=_('Model'),
                              related_name='specific_fields')
    datatype = models.ForeignKey(DataType,
                                 verbose_name=_('Data type'),
                                 related_name='model_specific_fields')

    class Meta:
        verbose_name = _('Model specific field')
        verbose_name_plural = _('Model specific fields')
        unique_together = ('model', 'name')

    def __repr__(self):
        return 'ModelSpecificField(%r, %r, %r, %r, %r)' % (
            self.name, self.minimum, self.maximum, self.model, self.datatype)


class ModelGlobalField(ModelGenericField):
    datatype = models.ForeignKey(DataType,
                                 verbose_name=_('Data type'),
                                 related_name='model_global_fields')

    class Meta:
        verbose_name = _('Model global field')
        verbose_name_plural = _('Model global fields')

    def __repr__(self):
        return 'ModelGlobalField(%r, %r, %r, %r)' % (
            self.name, self.minimum, self.maximum, self.datatype)


class ModelGlobalDatasetField(ModelGenericField):
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
    source = models.ForeignKey(Model,
                               verbose_name=_('Source'),
                               related_name='include')
    target = models.ForeignKey(Model,
                               verbose_name=_('Target'),
                               related_name='included_in')

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