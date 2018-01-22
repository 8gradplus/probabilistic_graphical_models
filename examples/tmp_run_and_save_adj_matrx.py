import pandas as pd
import networkx as nx
import json
import numpy as np
import sys
sys.path.append('..')
from graph.triangulation.variable_elimination import triangulate_variable_elimination
from helper.entropy import entropy_matrix

"""Helper functions for graph"""


def undirected_graph(adjecency: np.array):
    return nx.from_numpy_matrix(adjecency)


def largest_clique_size(G: nx.Graph):
    return max(clique_sizes(G))


def clique_sizes(G:nx.Graph):
    cliques = nx.find_cliques(G)
    return map(len, cliques)


def n_of_clique_memberships_for_node(cliques, node):
    return sum(node in clique for clique in cliques)


def n_of_clique_memberships(G:nx.Graph):
    cliques = list(nx.find_cliques(G))
    nodes = G.nodes
    return [(node, n_of_clique_memberships_for_node(cliques, node)) for node in nodes]


class AdjecencyMatrixFromEntropy:
    """Compute adjecency matrix as boolean array from entropy"""

    def __init__(self, threshold_index:int):
        self.threshold_index = threshold_index

    def __call__(self, entropy: np.array):
        sorted_entropy_values = np.flip(np.sort(entropy.flatten()), axis=0)
        threshold = sorted_entropy_values[self.threshold_index]
        return entropy >= threshold


def get_given_pixels(noisy_digit: np.array):
    given = dict()
    for i, d in np.ndenumerate(noisy_digit):
        if d < 2:
            given.update({i[0]: int(d)})
    return given


"""Helper functions for data"""

def read_json_file(path):
    with open(path, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
    return data


def randomize_digit(digit, n_pixels_to_remove = 8*20):
    randomized = digit.copy()
    mask=np.zeros(20*16, dtype=bool)
    mask[: n_pixels_to_remove] = True
    np.random.shuffle(mask)
    randomized[mask] = 5 # encode missing pixel with value 5
    return randomized


def randomize_digits(digits, n_pixels_to_remove_per_digit=8*20):
    randomized_digits = []
    for digit in range(digits.shape[0]):
        randomized = randomize_digit(digits[digit, :], n_pixels_to_remove_per_digit)
        randomized_digits.append(randomized)
    return np.array(randomized_digits)


def candidate_edges(M: np.array):
    flat_ids = reversed(list(np.argsort(M, axis=None)))
    ids = map(lambda i: np.unravel_index(i, M.shape), flat_ids)
    # Avoid duplicate edges in undirected graph by taking triangle of matrix
    return list(filter(lambda x: x[0] < x[1], ids))


def construct_trial_subgraph(g: nx.Graph, edge):
    t = g.copy()
    t.add_edge(*edge)
    subgraphs = nx.connected_component_subgraphs(t)
    filtered_subgraphs = [x for x in subgraphs if x.has_node(edge[0])]
    assert len(filtered_subgraphs) == 1, "Added edge is not contained in any subgraph"
    return filtered_subgraphs[0]


def thin_graph(nodes: iter, candidate_edges, width):
    """Find a thin triangulated graph by iteratively adding edges from sorted candidtate
    edges. If an added edge does not lead to a max cliquesize larger of width it is retained.
    oterwise it is ignored"""
    g = nx.Graph()
    g.add_nodes_from(nodes)

    n_edges = len(candidate_edges) # for verbose
    counter = 0  # for verbose
    for edge in candidate_edges:
        if g.has_edge(*edge):
            continue
        trial = construct_trial_subgraph(g, edge)
        if trial.number_of_edges() <= 3:
            continue
        triangulated = triangulate_variable_elimination(trial)
        if largest_clique_size(triangulated) < width:
            g.add_edges_from(triangulated.edges)

        # for verbose
        counter += 1
        if counter % 100 == 0:
            print("Done {counter} / {n_edges}".format(counter=counter, n_edges=n_edges))
    return g

def main():
    # threshold = int(sys.argv[1])
    raw = read_json_file(path='../data/binary_alpha_digits.txt')
    labels = np.array(raw['labels'])
    data = np.array(raw['data'])
    twos = data[labels == '2']
    matrix_of_pairwise_entropies = entropy_matrix(twos)

    for threshold in [10000, 20000, 30000, 40000, 50000]:
        candidates = list(candidate_edges(matrix_of_pairwise_entropies))[:threshold]
        thin_triangulation = thin_graph(range(320), candidates, 10)
        M = nx.to_numpy_matrix(thin_triangulation)
        P = pd.DataFrame(M)
        P.to_csv('adjecency_matrix_threshold_{0}.csv'.format(threshold), index=False, header=False)


if __name__ == "__main__":
    main()
