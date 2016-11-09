from django.conf import settings

from py2neo import Graph, NodeSelector, Transaction

g = Graph('http://localhost:7474/db/data', user=settings.NEO4J_USER, password=settings.NEO4J_PASS)
ns = NodeSelector(g)
tx = Transaction(g)
