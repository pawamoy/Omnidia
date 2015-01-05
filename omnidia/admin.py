from django.contrib import admin
from django.utils.translation import ugettext as _
from omnidia.models import (
    Dataset, DatasetValue, DataType, FileType,
    File, FileDatasetField, FileSpecificField,
    FileGlobalField, FileDatasetValue,
    FileSpecificValue, FileGlobalValue, Model,
    Object, ObjectLink, LinkData, ObjectFile,
    ModelDatasetField, ModelSpecificField,
    ModelGlobalField, ModelGlobalDatasetField,
    ModelModelField, ModelDatasetValue,
    ModelSpecificValue, ModelGlobalValue,
    ModelModelValue)


# Changing app labels
file_field = _('file_fields')
FileDatasetField._meta.app_label = file_field
FileSpecificField._meta.app_label = file_field
FileGlobalField._meta.app_label = file_field

model_field = _('model_fields')
ModelSpecificField._meta.app_label = model_field
ModelDatasetField._meta.app_label = model_field
ModelModelField._meta.app_label = model_field
ModelGlobalField._meta.app_label = model_field
ModelGlobalDatasetField._meta.app_label = model_field

file_value = _('file_values')
FileDatasetValue._meta.app_label = file_value
FileSpecificValue._meta.app_label = file_value
FileGlobalValue._meta.app_label = file_value

model_value = _('model_values')
ModelSpecificValue._meta.app_label = model_value
ModelDatasetValue._meta.app_label = model_value
ModelModelValue._meta.app_label = model_value
ModelGlobalValue._meta.app_label = model_value

# Creating admin classes

# Registering models
admin.site.register(Dataset)
admin.site.register(DatasetValue)
admin.site.register(DataType)
admin.site.register(FileType)
admin.site.register(File)
admin.site.register(FileDatasetField)
admin.site.register(FileSpecificField)
admin.site.register(FileGlobalField)
admin.site.register(FileDatasetValue)
admin.site.register(FileSpecificValue)
admin.site.register(FileGlobalValue)
admin.site.register(Model)
admin.site.register(Object)
admin.site.register(ObjectLink)
admin.site.register(LinkData)
admin.site.register(ObjectFile)
admin.site.register(ModelDatasetField)
admin.site.register(ModelSpecificField)
admin.site.register(ModelGlobalField)
admin.site.register(ModelGlobalDatasetField)
admin.site.register(ModelModelField)
admin.site.register(ModelDatasetValue)
admin.site.register(ModelSpecificValue)
admin.site.register(ModelGlobalValue)
admin.site.register(ModelModelValue)