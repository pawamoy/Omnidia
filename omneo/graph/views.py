from django.shortcuts import render, redirect
from django.urls import reverse

from py2neo import Node

from . import g, ns


def home(request):
    selection = ns.select()
    nodes_list = [
        {'id': id(node),
         'labels': [l for l in node.labels()],
         'properties': dict(node)}
        for node in selection
    ]

    return render(request, 'home.html', {'nodes': nodes_list})


def add(request):
    params = request.GET

    labels = params.get('labels', []).split()
    property1 = params.get('property1', None)
    value1 = params.get('value1', None)
    property2 = params.get('property2', None)
    value2 = params.get('value2', None)
    property3 = params.get('property3', None)
    value3 = params.get('value3', None)

    properties = {}
    if property1 and value1:
        properties[property1] = value1
    if property2 and value2:
        properties[property2] = value2
    if property3 and value3:
        properties[property3] = value3

    node = Node(*labels, **properties)

    g.create(node)

    return redirect(reverse('home'))


def delete(request, id):
    id = int(id)
    node = g.node(id)
    g.delete(node)
    return redirect(reverse('home'))


def search_persons(request, name):
    case_insensitive = True

    re_contains_name = '.*%s.*' % name

    if case_insensitive:
        re_contains_name = '(?i)' + re_contains_name

    persons_nodes = ns.select('Person')
    matching_persons = persons_nodes.where("_.name =~ '%s'" % re_contains_name)
    persons_list = list(matching_persons)

    return render(request, 'home.html', {'persons': persons_list})
