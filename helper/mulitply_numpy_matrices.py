import numpy as np
from .add_numpy_axis import add_axis


def multiply_vec(x: np.array, idx_x: list, y: np.array, idx_y: list):
    """Multiply two matrices x, y, taking care of different dimensions indicated by idx_x and id_y
    idx_x: list of dimension names for x
    idx_y: list of dimension names for y
    """
    idx = sorted(list(set(idx_x + idx_y)))
    print(idx)
    x_ext = add_axis(x, idx_x, idx)
    y_ext = add_axis(y, idx_y, idx)
    return x_ext * y_ext
