from . import g

COMING_IN = -1
BIDIRECTIONNAL = 0
GOING_TO = 1


def node_to_str(i, node, edges=True):
    node_id = 'n%d' % i if i >= 0 else ''

    node_string = '(%s:%s {%s})' % (
        node_id,
        ':'.join(node[0]),
        ','.join(('%s:"%s"' % (k, v) for k, v in node[1].items()))
    )

    if len(node) == 3 and edges:
        return '%s,%s' % (node_string, edge_to_str(node_id, node[2]))

    return node_string


def edge_to_str(node_id, edges):
    edge_strings = []
    for edge in edges:
        left_arrow = '<-' if edge[1] == COMING_IN else '-'
        right_arrow = '->' if edge[1] == GOING_TO else '-'
        edge_strings.append(','.join(['(%s)%s[:%s]%s%s' % (
            node_id,
            left_arrow,
            edge[0],
            right_arrow,
            node_to_str(-1, n, edges=False)
        ) for n in edge[2]]))
    return ','.join(edge_strings)


def create(nodes):
    """
    Create nodes and edges in batch.

    A node is of the following form: (labels (tuple), properties (dict), edges (tuple)).
    An edge is of the following form: (type (str), direction (const), nodes (tuple)).
    """
    nodes_string = ','.join((node_to_str(i, node) for i, node in enumerate(nodes)))

    query = 'CREATE %s' % nodes_string
    print(query)
    g.run(query)
