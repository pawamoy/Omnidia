import os

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Dataset, DatasetValue, File


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
            'values': dataset.text_values
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
