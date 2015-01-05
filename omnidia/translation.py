from modeltranslation.translator import translator, TranslationOptions
from omnidia.models import (
    Dataset, DatasetValue, DataType, FileType, File,
    FileDatasetField, FileSpecificField,
    FileGlobalField, FileSpecificValue, FileGlobalValue, Model,
    Object, ModelDatasetField, ModelSpecificField,
    ModelGlobalField, ModelGlobalDatasetField,
    ModelModelField, ModelSpecificValue, ModelGlobalValue)


class NameTranslation(TranslationOptions):
    fields = ('name', )


class ValueTranslation(TranslationOptions):
    fields = ('value', )


translator.register(Dataset, NameTranslation)
translator.register(DataType, NameTranslation)
translator.register(FileType, NameTranslation)
translator.register(File, NameTranslation)
translator.register(FileDatasetField, NameTranslation)
translator.register(FileSpecificField, NameTranslation)
translator.register(FileGlobalField, NameTranslation)
translator.register(Model, NameTranslation)
translator.register(Object, NameTranslation)
translator.register(ModelDatasetField, NameTranslation)
translator.register(ModelSpecificField, NameTranslation)
translator.register(ModelGlobalField, NameTranslation)
translator.register(ModelGlobalDatasetField, NameTranslation)
translator.register(ModelModelField, NameTranslation)
translator.register(DatasetValue, ValueTranslation)
translator.register(FileSpecificValue, ValueTranslation)
translator.register(FileGlobalValue, ValueTranslation)
translator.register(ModelSpecificValue, ValueTranslation)
translator.register(ModelGlobalValue, ValueTranslation)