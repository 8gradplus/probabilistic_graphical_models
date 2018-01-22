from itertools import combinations
import networkx as nx


def triangulate_variable_elimination(g: nx.graph):
    if nx.is_directed(g):
        raise nx.NetworkXException("Can only triangulate undirected graphs")
    t = g.copy()
    reducer = g.copy()
    triangulate_variable_elimination_rec(t, reducer)
    #assert nx.is_chordal(t), "Triangulation failed! Graph is not chordal"
    return t


def triangulate_variable_elimination_rec(g: nx.graph, r: nx.graph):
    """Recursively triangulate Graph via node elimination"""
    #if nx.is_chordal(g):
    #    return None
    if len(list(nx.find_cliques(r))) == 1:
        return None
    if len(list(r.nodes)) == 0:
        return None
    else:
        x = node_to_eliminate(r)
        # need to make list because iterator for missing_edges twice
        missing_edges = list(combinations(nx.neighbors(r, x), 2))
        g.add_edges_from(missing_edges)
        r.add_edges_from(missing_edges)
        r.remove_node(x)
        triangulate_variable_elimination_rec(g, r)


def n_missing_edges(g: nx.Graph, x):
    """Determine number of additional edges that that would be
    needed in order  to make the neighbors of x a clique.
    We use the fact that a clique has 1/2n(n-1) edges"""
    k = g.subgraph(g.neighbors(x))
    n = k.number_of_nodes()
    e = k.number_of_edges()
    return 0.5 * n * (n-1) - e


def elimination_order(g: nx.Graph):
    """Elimination order of nodes.
    The order is determined by the number of missing edges between
    neighbours of a node that would make the neighbors a clique"""
    missing = map(lambda x: (x, n_missing_edges(g, x)), g.nodes)
    return sorted(missing, key=lambda x: x[1])


def node_to_eliminate(g: nx.Graph):
    """Determines node to eliminate by taking the first node in the elimination order"""
    return elimination_order(g)[0][0]