import networkx as nx
import numpy as np


# Todo: refactor this! It's ugly, buggy, and stateful!

def most_probable_state(g: nx.Graph, given: dict=dict()):
    assert all(g.node[node]['potential'] is not None for node in g.nodes)
    assert all(g.node[node]['nodes'] is not None for node in g.nodes) # actually markov nodes /pixels
    assert all(type(v) is int for v in given.values())
    assert all(type(k) is int for k in given.keys())
    return Predict(g, given.copy()).predict().state()


class Predict:
    """If given dict is empty the result is the max prob solution"""

    def __init__(self, g: nx.DiGraph, given: dict=dict()):
        self.G = g.copy()
        self.maxima = given
        self.all_nodes = set(self.G.nodes)
        self.visited_nodes = set()

    def state(self):
        return np.array([self.maxima[pixel] for pixel in sorted(self.maxima.keys())])

    def is_determined(self, pixels: set):
        return pixels.issubset(set(self.maxima.keys()))

    def predict(self):
        for node in list(nx.dfs_preorder_nodes(self.G)):
            self.update_maxima(node)
            self.visited_nodes.add(node)
        return self

    def update_maxima(self, node):
        pot = self.G.node[node]['potential'].copy()
        pixels = self.G.node[node]['nodes'].copy()
        pixels_to_fix = [m for m in self.maxima.items() if m[0] in pixels]
        pot_residual, pixels_residual, _ = set_known_values(pot, pixels, pixels_to_fix)
        if pot_residual.shape:
            max_values = list(np.unravel_index(np.argmax(pot_residual), pot_residual.shape))
            for p, v in zip(pixels_residual, max_values):
                self.maxima.update({p: v})


def set_known_values(pot: np.array, pixels: list, pixels_to_fix):
    # either a function manipulates stuff OR it returns stuff. but not both!
    if pixels_to_fix:
        pixel, value = pixels_to_fix.pop(0)
        axis = pixels.index(pixel)
        pot = pot.take(indices=value, axis=axis)
        pixels.pop(pixels.index(pixel))
        return set_known_values(pot, pixels, pixels_to_fix)
    return pot, pixels, pixels_to_fix 