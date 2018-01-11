from unittest import TestCase
import networkx as nx
from graph.orient_junction_tree import orient_junction_tree


class TestJunctionTreeOrientation(TestCase):

    def test_orient_junction_tree_for_two_nodes_tree(self):
        g = nx.path_graph(2)
        r = orient_junction_tree(g)
        self.assertEqual(list(r.edges), [(0, 1)])

    def test_orient_junction_tree_for_complicated_tree(self):
        g = nx.Graph()
        g.add_nodes_from(range(5))
        g.add_edges_from([(1, 0), (2, 0), (3, 0), (4, 3)])
        r = orient_junction_tree(g)
        self.assertEqual(list(r.edges), [(0, 1), (0, 2), (0, 3), (3, 4)])

    def test_orient_junction_tree_fails_if_graph_is_not_a_tree(self):
        g = nx.Graph()
        g.add_nodes_from(range(2))
        self.assertRaises(AssertionError, lambda: orient_junction_tree(g))

    def test_orient_junction_tree_node_information_is_preserved(self):
        g = nx.Graph()
        g.add_nodes_from(range(2))
        g.add_edge(0, 1)
        g.node[0]['foo'] = 'bar'
        g.node[1]['foo'] = 'xbar'
        r = orient_junction_tree(g)
        self.assertTrue(r.node[0]['foo'] == 'bar')

    def test_orient_junction_tree_edge_information_is_preserved(self):
        g = nx.Graph()
        g.add_nodes_from(range(2))
        g.add_edge(0, 1, foo='bar')
        r = orient_junction_tree(g)
        self.assertTrue(r[0][1]['foo'] == 'bar')