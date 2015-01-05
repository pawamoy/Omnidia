from django.db import models
from django.utils.translation import ugettext_lazy as _
# TODO: set verbose_name and help_text, unicode/str method, other methods
# TODO: set related_name on foreign keys
# TODO: set verbose_name in Meta classes of models (translatable)


################################################################################
# OMNIDIA GENERAL

class Dataset(models.Model):
    name = models.CharField(max_length=30)


class DatasetValue(models.Model):
    # TODO: couples uniques
    dataset = models.ForeignKey(Dataset)
    value = models.CharField(max_length=255)


class DataType(models.Model):
    name = models.CharField(max_length=30)


################################################################################
# OMNIDIA FILES

class FileType(models.Model):
    name = models.CharField(_('File type'), max_length=30)


class File(models.Model):
    name = models.CharField(_('Filename'), max_length=255)
    link = models.CharField(_('File location'), max_length=255)
    type = models.ForeignKey(FileType, verbose_name=_('File type'))


################################################################################
# OMNIDIA FILE FIELDS

class FileGenericField(models.Model):
    name = models.CharField(_('Field name'), max_length=30)
    minimum = models.PositiveSmallIntegerField(_('Minimum'), default=0)
    maximum = models.PositiveSmallIntegerField(_('Maximum'), default=0)

    class Meta:
        abstract = True


class FileDatasetField(FileGenericField):
    # TODO: couples (filetype, name) uniques
    dataset = models.ForeignKey(Dataset)
    filetype = models.ForeignKey(FileType)


class FileSpecificField(FileGenericField):
    # TODO: couples (filetype, name) uniques
    filetype = models.ForeignKey(FileType)
    datatype = models.ForeignKey(DataType)


class FileGlobalField(FileGenericField):
    datatype = models.ForeignKey(DataType)


################################################################################
# OMNIDIA FILE VALUES

class FileGenericValue(models.Model):
    file = models.ForeignKey(File)

    class Meta:
        abstract = True


class FileDatasetValue(FileGenericValue):
    value = models.ForeignKey(DatasetValue)


class FileSpecificValue(FileGenericValue):
    field = models.ForeignKey(FileSpecificField)
    value = models.TextField()


class FileGlobalValue(FileGenericValue):
    field = models.ForeignKey(FileGlobalField)
    value = models.TextField()


################################################################################
# OMNIDIA MODELS

class Model(models.Model):
    name = models.CharField(max_length=30)


class Object(models.Model):
    name = models.CharField(max_length=255)
    model = models.ForeignKey(Model)


class ObjectLink(models.Model):
    # TODO: couples uniques
    object_ref1 = models.ForeignKey(Object, related_name='+')
    object_ref2 = models.ForeignKey(Object, related_name='+')


class LinkData(models.Model):
    link = models.ForeignKey(ObjectLink)
    # TODO: add fields here


class ObjectFile(models.Model):
    # TODO: couples uniques
    object = models.ForeignKey(Object)
    file = models.ForeignKey(File)


################################################################################
# OMNIDIA MODEL FIELDS

class ModelGenericField(models.Model):
    name = models.CharField(_('Field name'), max_length=30)
    minimum = models.PositiveSmallIntegerField(_('Minimum'), default=0)
    maximum = models.PositiveSmallIntegerField(_('Maximum'), default=0)

    class Meta:
        abstract = True


class ModelDatasetField(ModelGenericField):
    # TODO: couples (model, name) uniques
    dataset = models.ForeignKey(Dataset)
    model = models.ForeignKey(Model)


class ModelSpecificField(ModelGenericField):
    # TODO: couples (model, name) uniques
    model = models.ForeignKey(Model)
    datatype = models.ForeignKey(DataType)


class ModelGlobalField(ModelGenericField):
    datatype = models.ForeignKey(DataType)


class ModelGlobalDatasetField(ModelGenericField):
    dataset = models.ForeignKey(Dataset)


class ModelModelField(ModelGenericField):
    # TODO: couples (source, name) uniques
    source = models.ForeignKey(Model, related_name='+')
    target = models.ForeignKey(Model, related_name='+')


################################################################################
# OMNIDIA MODEL VALUES

class ModelGenericValue(models.Model):
    object = models.ForeignKey(Object)

    class Meta:
        abstract = True


class ModelDatasetValue(ModelGenericValue):
    value = models.ForeignKey(DatasetValue)
    field = models.ForeignKey(ModelDatasetField)


class ModelSpecificValue(ModelGenericValue):
    field = models.ForeignKey(ModelSpecificField)
    value = models.TextField()


class ModelGlobalValue(ModelGenericValue):
    field = models.ForeignKey(ModelGlobalField)
    value = models.TextField()


class ModelModelValue(ModelGenericValue):
    field = models.ForeignKey(ModelModelField, related_name='+')
    value = models.ForeignKey(Object, related_name='+')