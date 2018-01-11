import numpy as np
import networkx as nx
from helper.empirical_distribution import empirical_distribution

"""Currently we assume for the nodes of the underlying markov network are
1) still carried around in the junction tree
2) the nodes may be associated with the data as indices
"""
#Todo: generalize this


def assign_clique_potentials(data: np.array, t:nx.Graph):
    """Assign clique potentials on nodes of junction tree / clique graph"""
    r = t.copy()
    for node in r.nodes:
        markov_nodes = r.node[node]['nodes']
        r.node[node]['clique_potential'] = empirical_distribution(data[:, markov_nodes])
    return r


def assign_seperator_potentials(data: np.array, t: nx.Graph):
    """Assign seperator potentials on edges of junction tree / clique graph"""
    r = t.copy()
    for edge in r.edges:
        edge_attr = r[edge[0]][edge[1]]
        markov_nodes = edge_attr['intersection']
        edge_attr['seperator_potential'] = empirical_distribution(data[:, markov_nodes])
    return r


class AssignPotentials:
    """Assign clique potentials and seperator potentials on junction tree / clique graph"""

    def __init__(self, data):
        self.data = data

    def __call__(self, t: nx.Graph):
        junction_tree = assign_clique_potentials(self.data, t)
        return assign_seperator_potentials(self.data, junction_tree)