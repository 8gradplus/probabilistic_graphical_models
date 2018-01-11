import networkx as nx


def to_junction_tree(g: nx.Graph):
    """Compute junction tree from a clique graph.
    This is the maximum weight spanning tree of the clique graph with edge weights
    being the size if the intersection between two nodes"""
    return nx.maximum_spanning_tree(g, weight='weight', algorithm='kruskal')