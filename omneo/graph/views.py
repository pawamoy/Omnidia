from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Dataset


def home(request):
    return datasets(request)


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


def datasets(request):
    dataset_list = [
        {
            'name': dataset.name,
            'values': dataset.values
        }
        for dataset in Dataset.all()
    ]

    return render(request, 'home.html', {'datasets': dataset_list})


def add_dataset(request):
    params = request.GET
    dataset = Dataset.create(name=params.get('name'))

    value1 = params.get('value1', None)
    value2 = params.get('value2', None)
    value3 = params.get('value3', None)

    for value in (value1, value2, value3):
        if value:
            dataset.add_value(value)

    return redirect(reverse('datasets:main'))


def delete_dataset(request, name):
    dataset = Dataset.get(name)
    if dataset:
        dataset.delete()
    return redirect(reverse('datasets:main'))
