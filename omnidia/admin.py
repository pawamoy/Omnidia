from django.contrib import admin
from django.utils.translation import ugettext as _
from omnidia.models import (
    Dataset, DatasetValue, FileType,
    File, FileDatasetValue, Model, Object,
    ModelDatasetField, FileTypeDatasetField, FileTypeField, FileValue,
    ModelField, ObjectDatasetValue, ObjectValue)


admin.site.register(Dataset)
admin.site.register(DatasetValue)
admin.site.register(FileType)
admin.site.register(File)
admin.site.register(FileTypeDatasetField)
admin.site.register(FileTypeField)
admin.site.register(FileDatasetValue)
admin.site.register(FileValue)
admin.site.register(Model)
admin.site.register(Object)
admin.site.register(ModelDatasetField)
admin.site.register(ModelField)
admin.site.register(ObjectDatasetValue)
admin.site.register(ObjectValue)