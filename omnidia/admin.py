from django.contrib import admin
from django.utils.translation import ugettext as _
from omnidia.models import (
    Dataset, DatasetValue, FileType,
    File, FileDatasetValue, Model, Object,
    ModelDatasetField, FileTypeDatasetField, FileTypeField, FileValue,
    ModelField, ObjectDatasetValue, ObjectValue)


class DatasetValueInline(admin.TabularInline):
    model = DatasetValue
    extra = 0


class DatasetAdmin(admin.ModelAdmin):
    list_display = ('name', 'datatype')
    list_editable = ('name', 'datatype')
    inlines = (DatasetValueInline, )


class DatasetValueAdmin(admin.ModelAdmin):
    list_display = ('dataset', 'value')
    list_editable = ('value', )


class FileTypeFieldInline(admin.TabularInline):
    model = FileTypeField
    extra = 0


class FileTypeDatasetFieldInline(admin.TabularInline):
    model = FileTypeDatasetField
    extra = 0


class FileTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_editable = ('name', )
    inlines = (FileTypeFieldInline, FileTypeDatasetFieldInline)


admin.site.register(Dataset, DatasetAdmin)
admin.site.register(DatasetValue, DatasetValueAdmin)
admin.site.register(FileType, FileTypeAdmin)
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