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