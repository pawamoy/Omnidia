from django.shortcuts import render, redirect

from py2neo import Node

from . import g, ns


def persons(request):
    selection = ns.select('Person')
    persons_list = list(selection)
    return render(request, 'home.html', {'persons': persons_list})


def add_person(request, person):
    p = Node('Person', name=person)
    g.create(p)
    return redirect('/persons')


def search_persons(request, name):
    case_insensitive = True

    re_contains_name = '.*%s.*' % name

    if case_insensitive:
        re_contains_name = '(?i)' + re_contains_name

    persons_nodes = ns.select('Person')
    matching_persons = persons_nodes.where("_.name =~ '%s'" % re_contains_name)
    persons_list = list(matching_persons)

    return render(request, 'home.html', {'persons': persons_list})
