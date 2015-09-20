from modeltranslation.translator import translator, TranslationOptions
from omnidia.models import (
    Dataset, DatasetValue, FileType, File, Model, Object, ModelDatasetField,
    FileTypeDatasetField, FileTypeField, FileValue, ModelField, ObjectValue)


class NameTranslation(TranslationOptions):
    fields = ('name', )


class ValueTranslation(TranslationOptions):
    fields = ('value', )


translator.register(Dataset, NameTranslation)
translator.register(FileType, NameTranslation)
translator.register(File, NameTranslation)
translator.register(FileTypeDatasetField, NameTranslation)
translator.register(FileTypeField, NameTranslation)
translator.register(Model, NameTranslation)
translator.register(Object, NameTranslation)
translator.register(ModelDatasetField, NameTranslation)
translator.register(ModelField, NameTranslation)
translator.register(DatasetValue, ValueTranslation)
translator.register(FileValue, ValueTranslation)
translator.register(ObjectValue, ValueTranslation)