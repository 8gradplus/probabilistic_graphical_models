import numpy as np


def add_axis(x: np.array, indices, ext_indices):
    """Adds numpy (dummy) dimensions for vectorized handling of proababilty tables"""
    assert set(indices) <= set(ext_indices), "Seperator variables are not a subset of clique variables"
    axes = [ext_indices.index(a) for a in ext_indices if a not in indices]
    r = x.copy()
    for axis in axes:
        r = np.expand_dims(r, axis)
    return r