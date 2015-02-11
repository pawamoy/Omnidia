from django.db import models
from django.utils.translation import ugettext_lazy as _
# TODO: set verbose_name and help_text, unicode/str method, other methods
# TODO: set related_name on foreign keys
# TODO: set verbose_name in Meta classes of models (translatable)


################################################################################
# OMNIDIA GENERAL

class DataType(models.Model):
    DATATYPE_CHOICES = (
        ['text', _('Text')],
        ['date', _('Date')],
        ['datetime', _('Datetime')],
        ['time', _('Time')],
        ['integer', _('Integer')],
        ['float', _('Float')],
        ['binary', _('Binary')],
    )
    name = models.CharField(max_length=30, choices=DATATYPE_CHOICES)

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'DataType(%r)' % self.name


class Dataset(models.Model):
    name = models.CharField(max_length=30)
    datatype = models.ForeignKey(DataType, related_name='datasets')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Dataset(%r, %r)' % (self.name, self.datatype)


class DatasetValue(models.Model):
    dataset = models.ForeignKey(Dataset, related_name='values')
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('dataset', 'value')

    def __str__(self):
        return self.value

    def __repr__(self):
        return 'DatasetValue(%r, %r)' % (self.dataset, self.value)


################################################################################
# OMNIDIA FILES

class FileType(models.Model):
    name = models.CharField(_('File type'), max_length=30)

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'FileType(%r)' % self.name


class File(models.Model):
    name = models.CharField(_('Filename'), max_length=255)
    # TODO: FieldField or FilePathField ?
    file = models.FileField(_('File location'))
    type = models.ForeignKey(FileType, verbose_name=_('File type'))
    hash = models.CharField(_('SHA256 Hash'), max_length=256)

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'File(%r, %r, %r, %r)' % (self.name, self.file,
                                         self.type, self.hash)


################################################################################
# OMNIDIA FILE FIELDS

class FileGenericField(models.Model):
    name = models.CharField(_('Field name'), max_length=30)
    minimum = models.PositiveSmallIntegerField(_('Minimum'), default=0)
    maximum = models.PositiveSmallIntegerField(_('Maximum'), default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'FileGenericField(%r, %r, %r)' % (
            self.name, self.minimum, self.maximum)


class FileDatasetField(FileGenericField):
    dataset = models.ForeignKey(Dataset, related_name='file_fields')
    filetype = models.ForeignKey(FileType, related_name='dataset_fields')

    class Meta:
        unique_together = ('filetype', 'name')

    def __repr__(self):
        return 'FileDatasetField(%r, %r, %r, %r, %r)' % (
            self.name, self.minimum, self.maximum, self.dataset, self.filetype)


class FileSpecificField(FileGenericField):
    filetype = models.ForeignKey(FileType, related_name='specific_fields')
    datatype = models.ForeignKey(DataType, related_name='file_specific_fields')

    class Meta:
        unique_together = ('filetype', 'name')

    def __repr__(self):
        return 'FileSpecificField(%r, %r, %r, %r, %r)' % (
            self.name, self.minimum, self.maximum, self.filetype, self.datatype)


class FileGlobalField(FileGenericField):
    datatype = models.ForeignKey(DataType, related_name='file_global_fields')

    def __repr__(self):
        return 'FileGlobalField(%r, %r, %r, %r)' % (
            self.name, self.minimum, self.maximum, self.dataype)


################################################################################
# OMNIDIA FILE VALUES

class FileGenericValue(models.Model):
    file = models.ForeignKey(File)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return 'FileDatasetValue(%r)' % self.file


class FileDatasetValue(FileGenericValue):
    value = models.ForeignKey(DatasetValue, related_name='file_values')

    def __repr__(self):
        return 'FileDatasetField(%r, %r)' % (self.file, self.value)


class FileSpecificValue(FileGenericValue):
    field = models.ForeignKey(FileSpecificField, related_name='values')
    value = models.TextField()

    def __repr__(self):
        return 'FileSpecificField(%r, %r, %r)' % (
            self.file, self.field, self.value)


class FileGlobalValue(FileGenericValue):
    field = models.ForeignKey(FileGlobalField, related_name='values')
    value = models.TextField()

    def __repr__(self):
        return 'FileGlobalField(%r, %r, %r)' % (
            self.file, self.field, self.value)


class FileGlobalDatasetField(FileGenericField):
    dataset = models.ForeignKey(Dataset, related_name='file_global_fields')

    def __repr__(self):
        return 'FileDatasetField(%r, %r)' % (self.file, self.dataset)


################################################################################
# OMNIDIA MODELS

class Model(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Model(%r)' % self.name


class Object(models.Model):
    name = models.CharField(max_length=255)
    model = models.ForeignKey(Model, related_name='objects')

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Object(%r, %r)' % (self.name, self.model)


class ObjectLink(models.Model):
    object_ref1 = models.ForeignKey(Object, related_name='links_to')
    object_ref2 = models.ForeignKey(Object, related_name='links_from')

    class Meta:
        unique_together = ('object_ref1', 'object_ref2')

    def __str__(self):
        return '%s - %s' % (self.object_ref1, self.object_ref2)

    def __repr__(self):
        return 'ObjectLink(%r, %r)' % (self.object_ref1, self.object_ref2)


class LinkData(models.Model):
    link = models.ForeignKey(ObjectLink, related_name='data')
    # TODO: add fields here

    def __str__(self):
        return str(self.link)

    def __repr__(self):
        return 'LinkData(%r)' % self.link


class ObjectFile(models.Model):
    object = models.ForeignKey(Object, related_name='files')
    file = models.ForeignKey(File, related_name='objects')

    class Meta:
        unique_together = ('object', 'file')

    def __str__(self):
        return '%s - %s' % (self.object, self.file)

    def __repr__(self):
        return 'ObjectFile(%r, %r)' % (self.object, self.file)


################################################################################
# OMNIDIA MODEL FIELDS

class ModelGenericField(models.Model):
    name = models.CharField(_('Field name'), max_length=30)
    minimum = models.PositiveSmallIntegerField(_('Minimum'), default=0)
    maximum = models.PositiveSmallIntegerField(_('Maximum'), default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'ModelField(%r, %r, %r)' % (
            self.name, self.minimum, self.maximum)


class ModelDatasetField(ModelGenericField):
    dataset = models.ForeignKey(Dataset, related_name='model_fields')
    model = models.ForeignKey(Model, related_name='dataset_fields')

    class Meta:
        unique_together = ('model', 'name')


class ModelSpecificField(ModelGenericField):
    model = models.ForeignKey(Model, related_name='specific_fields')
    datatype = models.ForeignKey(DataType, related_name='model_specific_fields')

    class Meta:
        unique_together = ('model', 'name')


class ModelGlobalField(ModelGenericField):
    datatype = models.ForeignKey(DataType, related_name='model_global_fields')


class ModelGlobalDatasetField(ModelGenericField):
    dataset = models.ForeignKey(Dataset, related_name='model_global_fields')


class ModelModelField(ModelGenericField):
    source = models.ForeignKey(Model, related_name='include')
    target = models.ForeignKey(Model, related_name='included_in')

    class Meta:
        unique_together = ('source', 'name')


################################################################################
# OMNIDIA MODEL VALUES

class ModelGenericValue(models.Model):
    object = models.ForeignKey(Object)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.value)


class ModelDatasetValue(ModelGenericValue):
    value = models.ForeignKey(DatasetValue, related_name='model_values')
    field = models.ForeignKey(ModelDatasetField, related_name='values')


class ModelSpecificValue(ModelGenericValue):
    field = models.ForeignKey(ModelSpecificField, related_name='values')
    value = models.TextField()


class ModelGlobalValue(ModelGenericValue):
    field = models.ForeignKey(ModelGlobalField, related_name='values')
    value = models.TextField()


class ModelGlobalDatasetValue(ModelGenericValue):
    field = models.ForeignKey(ModelGlobalDatasetField, related_name='values')
    value = models.ForeignKey(DatasetValue, related_name='model_global_values')


class ModelModelValue(ModelGenericValue):
    field = models.ForeignKey(ModelModelField, related_name='values')
    value = models.ForeignKey(Object, related_name='value_of')