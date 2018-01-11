import networkx as nx
import numpy as np
from helper.add_numpy_axis import add_axis

# Todo: make this more generic, similar as in assign_potentials


def pass_message(edge, node):
    """ Pass seperator potential to clique graph.
    This just computes the conditional entropy p(clique | seperator).
    Thus the probability tables are divided taking care of the proper index structure.
    """
    extended_sep_pot = add_axis(edge['seperator_potential'], edge['intersection'], node['nodes'])
    clique_pot = node['clique_potential']
    default = np.zeros_like(clique_pot)
    msg = "After extension clique and seperator potentials differ in dimensions"
    assert len(clique_pot.shape) == len(extended_sep_pot.shape), msg
    return np.divide(clique_pot, extended_sep_pot, out=default, where=extended_sep_pot != 0)


def adsorb_separator_potentials(d: nx.DiGraph):
    assert nx.is_directed(d), 'Can only pass messages on oriented junction tree'
    r = d.copy()
    for node in r.nodes:
        parents = list(r.predecessors(node))
        if parents:
            assert len(parents) == 1, "There are multiple parents for node {node}".format(node=node)
            r.node[node]['potential'] = pass_message(r[parents[0]][node], r.node[node])
            r.node[node]['conditioned on'] = set(r[parents[0]][node]['intersection'])
        else:
            r.node[node]['potential'] = r.node[node]['clique_potential']
            r.node[node]['conditioned on'] = set()
    return r