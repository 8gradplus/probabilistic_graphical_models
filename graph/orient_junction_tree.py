import networkx as nx


def orient_junction_forest(ts: nx.Graph):
    """Orients a junction forest by orienting each connected subgraph seperately"""
    oriented_trees = map(lambda g: orient_junction_tree(g),
                         nx.connected_component_subgraphs(ts))
    return nx.compose_all(list(oriented_trees))


def orient_junction_tree(t: nx.Graph):
    """Make oriented Junction tree out of an unoriented Junction tree,
    preserving node and edge informations"""
    assert nx.is_tree(t), "Graph must have tree structure"
    oriented = nx.bfs_tree(t, list(t.nodes)[0])
    for n in oriented.nodes:
        oriented.node[n].update(t.node[n])
    for e in oriented.edges:
        oriented[e[0]][e[1]].update(t[e[0]][e[1]])
    return oriented 