from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Dataset, DatasetValue, File, Object


# def search_persons(request, name):
#     case_insensitive = True
#
#     re_contains_name = '.*%s.*' % name
#
#     if case_insensitive:
#         re_contains_name = '(?i)' + re_contains_name
#
#     persons_nodes = g.find('Person')
#     matching_persons = persons_nodes.where("_.name =~ '%s'" % re_contains_name)
#     persons_list = list(matching_persons)
#
#     return render(request, 'home.html', {'persons': persons_list})

def home(request):
    return render(request, 'home.html')


def datasets(request):
    dataset_list = [
        {
            'name': dataset.name,
            'values': sorted([(dv.name, dv.is_premium) for dv in dataset.values],
                             key=lambda x: x[0])
        }
        for dataset in Dataset.all()
    ]

    return render(request, 'datasets.html', {'datasets': dataset_list})


def dataset_add(request):
    params = request.GET
    Dataset.create(name=params.get('name'))

    return redirect(reverse('datasets:main'))


def dataset_details(request, dataset):
    pass


def dataset_delete(request, dataset):
    dataset = Dataset.get(name=dataset)
    if dataset:
        dataset.delete()
    return redirect(reverse('datasets:main'))


def dataset_values(request, dataset):
    pass


def value_add(request, dataset):
    dataset = Dataset.get(name=dataset)
    if dataset:
        value = request.GET.get('name')
        dataset.add_value(value)
    return redirect(reverse('datasets:main'))


def value_details(request, dataset, value):
    pass


def value_delete(request, dataset, value):
    dataset = Dataset.get(name=dataset)
    value = DatasetValue.get(name=value)
    if dataset and value:
        dataset.separate_value(value)
    return redirect(reverse('datasets:main'))


def value_toggle_premium(request, dataset, value):
    dataset = Dataset.get(name=dataset)
    value = DatasetValue.get(name=value)
    if dataset and value:
        value.is_premium = not value.is_premium
        value.save()
    return redirect(reverse('datasets:main'))


def files(request):
    files_list = [
        {
            'name': file.name,
            'path': file.path,
            'file_hash': file.file_hash,
            'path_hash': file.path_hash
        }
        for file in File.all()
    ]
    return render(request, 'files.html', {'files': files_list})


def file_details(request):
    return None


def file_delete(request, path_hash):
    file = File.get(path_hash=path_hash)
    if file:
        file.delete()
    return redirect(reverse('files:main'))


def objects(request):
    objects_list = [
        {
            'name': obj.name,
        }
        for obj in Object.all()
    ]
    return render(request, 'objects.html', {'objects': objects_list})


def object_add(request):
    params = request.POST
    Object.create(name=params.get('name'))

    return redirect(reverse('objects:main'))


def object_details(request):
    return None


def object_delete(request, name):
    obj = Object.get(name=name)
    if obj:
        obj.delete()
    return redirect(reverse('objects:main'))
