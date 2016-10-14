from py2neo import Graph, NodeSelector

g = Graph(user='neo4j', password='admineo4j')
ns = NodeSelector(g)
