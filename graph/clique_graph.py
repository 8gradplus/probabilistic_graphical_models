import networkx as nx
from itertools import combinations


def to_clique_graph(t: nx.Graph):
    """Compute clique graph from a triangulated graph T"""
    g = nx.Graph()
    cliques = list(enumerate(set(c) for c in nx.find_cliques(t)))
    g.add_nodes_from((i, {'nodes': sorted(list(c))}) for i, c in cliques)
    clique_pairs = combinations(cliques, 2)
    edges = ((i, j, c1 & c2) for (i, c1), (j, c2) in clique_pairs if c1 & c2)
    for edge in edges:
        g.add_edge(edge[0], edge[1], weight=len(edge[2]), intersection=sorted(list(edge[2])))
    return g
