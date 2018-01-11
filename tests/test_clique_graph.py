from unittest import TestCase
import networkx as nx
from itertools import combinations
from graph.clique_graph import to_clique_graph


class TestCliqueGraph(TestCase):

    def test_3_clique_has_exactly_one_node(self):
        g = nx.Graph()
        g.add_nodes_from(range(3))
        g.add_edges_from(combinations(range(3), 2))
        r = to_clique_graph(g)
        self.assertEqual(len(r.nodes), 1)
        self.assertEqual(r.node[0]['nodes'], list(range(3)))

    def test_two_cliques_that_have_one_node_in_common(self):
        g = nx.Graph()
        g.add_nodes_from(range(5))
        g.add_edges_from(combinations(range(3), 2))
        g.add_edges_from(combinations(range(2, 5), 2))
        r = to_clique_graph(g)
        self.assertEqual(len(r.edges), 1)
        self.assertEqual(len(r.nodes), 2)
        self.assertEqual(list(r.edges(data='weight')), [(0, 1, 1)])