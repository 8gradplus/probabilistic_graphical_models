import numpy as np
from itertools import product
from helper.empirical_distribution import empirical_distribution
from scipy.stats import entropy


def pairwise_entropy(a: np.array):
    contingency = empirical_distribution(a)
    ps = contingency.flatten()
    return entropy(ps)


def entropy_matrix(training):
    """Computes entropy matrix for each pixel tupel - Needs vectorization!"""
    shape = training.shape[1]
    e = np.zeros((shape, shape))
    for i, j in product(*map(range, (shape, shape))):
        a = training[:, [i, j]]
        e[i, j] = pairwise_entropy(a)
    return e