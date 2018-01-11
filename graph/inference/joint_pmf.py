from helper.mulitply_numpy_matrices import multiply_vec
import networkx as nx

# Warning! don't do this for graphs which are not exceptionally small clique potentials - your memory will explode!


def joint_pmf(g: nx.Graph):
    """Compute the joint probability mass function (tensor) on junction tree potentials"""
    nodes = list(g.nodes)
    pmf, idx_visited = extract_node_info(g, nodes.pop(0))
    for node in nodes:
        pot, idx = extract_node_info(g, node)
        pmf = multiply_vec(pmf, idx_visited, pot, idx)
        idx_visited = sorted(list(set(idx_visited + idx)))
    return pmf


def extract_node_info(g: nx.Graph, node):
    pot = g.node[node]['potential']
    ns = g.node[node]['nodes']
    return pot, sorted(ns)