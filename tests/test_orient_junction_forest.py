from unittest import TestCase
import networkx as nx
from graph.orient_junction_tree import orient_junction_forest


class TestJunctionForestOrientation(TestCase):

    def test_orient_junction_forest_for_two_isolated_nodes(self):
        g = nx.Graph()
        g.add_nodes_from(range(2))
        r = orient_junction_forest(g)
        self.assertEqual(set(r.nodes), set(range(2)))
        self.assertEqual(list(r.edges), [])

    def test_non_connected_graph_does_orientation_connected_subgraph_wise(self):
        g = nx.Graph()
        g.add_nodes_from(range(3))
        g.add_edge(1, 2)
        r = orient_junction_forest(g)
        self.assertEqual(set(r.nodes), set(range(3)))
        self.assertEqual(list(r.edges), [(1, 2)])