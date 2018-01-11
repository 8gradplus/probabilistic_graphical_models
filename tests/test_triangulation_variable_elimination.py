from unittest import TestCase
import networkx as nx
from itertools import combinations
import numpy as np
from graph.triangulation.variable_elimination import elimination_order, n_missing_edges
from graph.triangulation.variable_elimination import triangulate_variable_elimination


class TestTriangulateVariableElimination(TestCase):
    """Some tests: note that methods must have prefix 'test' in order to
    be recongniced as a test"""

    def test_elimination_order_for_single_node(self):
        g = nx.Graph()
        g.add_node(0)
        self.assertEqual(list(elimination_order(g)), [(0, 0)])

    def test_elimination_order_for_two_connected_nodes(self):
        g = nx.Graph()
        g.add_nodes_from(range(2))
        g.add_edge(0, 1)
        self.assertEqual(list(elimination_order(g)), [(0, 0), (1, 0)])

    def test_elemination_order_for_3_clique(self):
        g = nx.Graph()
        g.add_nodes_from(range(3))
        g.add_edges_from(combinations(range(3), 2))
        self.assertEqual(set(elimination_order(g)), {(0, 0), (1, 0), (2, 0)})

    def test_elemination_order_for_V_graph(self):
        g = nx.Graph()
        g.add_nodes_from(range(3))
        g.add_edges_from([(0, 1), (0, 2)])
        self.assertEqual(set(elimination_order(g)), {(0, 1), (1, 0), (2, 0)})

    def test_elemination_order_for_V_graph_has_highest_order_at_collider(self):
        g = nx.Graph()
        g.add_nodes_from(range(3))
        g.add_edges_from([(0, 1), (0, 2)])
        self.assertEqual(elimination_order(g)[-1], (0, 1))

    def test_3_clique_has_no_missing_edges(self):
        m = np.ones((3, 3))
        np.fill_diagonal(m, 0)
        g = nx.Graph(m)
        self.assertEqual(n_missing_edges(g, 0), 0)

    def test_V_graph_has_1_missing_edge(self):
        g = nx.Graph()
        g.add_nodes_from(range(3))
        g.add_edges_from([(0, 1), (0, 2)])
        self.assertEqual(n_missing_edges(g, 0), 1)

    def test_single_node_has_no_missing_edge(self):
        g = nx.Graph()
        g.add_node(0)
        self.assertEqual(n_missing_edges(g, 0), 0)

    def test_two_connected_nodes_have_no_missing_edge(self):
        g = nx.Graph()
        g.add_nodes_from(range(2))
        g.add_edge(0, 1)
        self.assertEqual(n_missing_edges(g, 0), 0)

    def test_triangulation_of_3_clique_maps_on_itself(self):
        m = np.ones((3, 3))
        np.fill_diagonal(m, 0)
        g = nx.Graph(m)
        t = triangulate_variable_elimination(g)
        self.assertTrue((m == nx.to_numpy_array(t)).all())
        self.assertTrue(nx.is_chordal(t))

    def test_triangulation_of_square_adds_one_edge(self):
        g = nx.Graph()
        g.add_nodes_from(range(4))
        g.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])
        t = triangulate_variable_elimination(g)
        self.assertTrue(t.number_of_edges() == 5)
        self.assertTrue(nx.is_chordal(t))

    def test_triangulation_of_square_and_isolated_node_is_chordal(self):
        g = nx.Graph()
        g.add_nodes_from(range(5))
        g.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])
        t = triangulate_variable_elimination(g)
        self.assertTrue(nx.is_chordal(t))