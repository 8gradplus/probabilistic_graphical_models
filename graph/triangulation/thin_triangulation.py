import networkx as nx
from graph.triangulation.variable_elimination import triangulate_variable_elimination


def construct_trial_subgraph(g: nx.Graph, edge):
    t = g.copy()
    t.add_edge(*edge)
    subgraphs = nx.connected_component_subgraphs(t)
    filtered_subgraphs = [x for x in subgraphs if x.has_node(edge[0])]
    assert len(filtered_subgraphs) == 1, "Added edge is not contained in any subgraph"
    return filtered_subgraphs[0]


def largest_clique_size(g: nx.Graph):
    return max(map(len, nx.find_cliques(g)))


def thin_graph(nodes: iter, candidate_edges, width):
    """Find a thin triangulated graph by iteratively adding edges from sorted candidtate edges.
    If an added edge does not lead to a max cliquesize larger of width it is retained, oterwise it is ignored"""
    g = nx.Graph()
    g.add_nodes_from(nodes)

    counter = 0
    n_edges = len(candidate_edges)
    for edge in candidate_edges:
        counter += 1
        if counter % 100 == 0:
            print("Finished {counter} / {total} edges". format(counter=counter, total=n_edges))
        if g.has_edge(*edge):
            continue
        trial = construct_trial_subgraph(g, edge)
        if trial.number_of_edges() <= 3:
            g.add_edge(*edge)
            continue
        triangulated = triangulate_variable_elimination(trial)
        if largest_clique_size(triangulated) - 1 <= width:
            g.add_edges_from(triangulated.edges)
    return g 