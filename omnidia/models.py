from django.db import models
from django.utils.translation import ugettext_lazy as _
# TODO: set verbose_name and help_text, unicode/str method, other methods
# TODO: set related_name on foreign keys
# TODO: set verbose_name in Meta classes of models (translatable)


################################################################################
# OMNIDIA GENERAL

class DataType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Dataset(models.Model):
    name = models.CharField(max_length=30)
    datatype = models.ForeignKey(DataType, related_name='datasets')

    def __str__(self):
        return self.name


class DatasetValue(models.Model):
    dataset = models.ForeignKey(Dataset, related_name='values')
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('dataset', 'value')

    def __str__(self):
        return self.value


################################################################################
# OMNIDIA FILES

class FileType(models.Model):
    name = models.CharField(_('File type'), max_length=30)

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(_('Filename'), max_length=255)
    # TODO: FieldField or FilePathField ?
    file = models.FileField(_('File location'))
    type = models.ForeignKey(FileType, verbose_name=_('File type'))
    hash = models.CharField(_('SHA256 Hash'), max_length=256)

    def __str__(self):
        return self.name


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


class FileDatasetField(FileGenericField):
    dataset = models.ForeignKey(Dataset, related_name='file_fields')
    filetype = models.ForeignKey(FileType, related_name='dataset_fields')

    class Meta:
        unique_together = ('filetype', 'name')


class FileSpecificField(FileGenericField):
    filetype = models.ForeignKey(FileType, related_name='specific_fields')
    datatype = models.ForeignKey(DataType, related_name='file_specific_fields')

    class Meta:
        unique_together = ('filetype', 'name')


class FileGlobalField(FileGenericField):
    datatype = models.ForeignKey(DataType, related_name='file_global_fields')


################################################################################
# OMNIDIA FILE VALUES

class FileGenericValue(models.Model):
    file = models.ForeignKey(File)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.value)


class FileDatasetValue(FileGenericValue):
    value = models.ForeignKey(DatasetValue, related_name='file_values')


class FileSpecificValue(FileGenericValue):
    field = models.ForeignKey(FileSpecificField, related_name='values')
    value = models.TextField()


class FileGlobalValue(FileGenericValue):
    field = models.ForeignKey(FileGlobalField, related_name='values')
    value = models.TextField()


################################################################################
# OMNIDIA MODELS

class Model(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Object(models.Model):
    name = models.CharField(max_length=255)
    model = models.ForeignKey(Model, related_name='objects')

    def __str__(self):
        return self.name


class ObjectLink(models.Model):
    object_ref1 = models.ForeignKey(Object, related_name='links_to')
    object_ref2 = models.ForeignKey(Object, related_name='links_from')

    class Meta:
        unique_together = ('object_ref1', 'object_ref2')

    def __str__(self):
        return '%s - %s' % (str(self.object_ref1), str(self.object_ref2))


class LinkData(models.Model):
    link = models.ForeignKey(ObjectLink, related_name='data')
    # TODO: add fields here

    def __str__(self):
        return str(self.link)


class ObjectFile(models.Model):
    object = models.ForeignKey(Object, related_name='files')
    file = models.ForeignKey(File, related_name='objects')

    class Meta:
        unique_together = ('object', 'file')

    def __str__(self):
        return '%s - %s' % (str(self.object), str(self.file))


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


class ModelModelValue(ModelGenericValue):
    field = models.ForeignKey(ModelModelField, related_name='values')
    value = models.ForeignKey(Object, related_name='value_of')