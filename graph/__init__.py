from py2neo import Graph, NodeSelector

g = Graph('http://localhost:7474/db/data', user='neo4j', password='admineo4j')
ns = NodeSelector(g)
