import numpy as np

'''
def empirical_distribution(a: np.array):
    """Empirical discrete distribution for arbitrary dimensions"""
    tensor = a.copy()
    if len(a.shape) == 1:
        tensor = np.reshape(a, (a.shape[0], 1))
    result = np.zeros(tensor.shape[1]*[2])
    counts = np.unique(tensor, return_counts=True, axis=0)
    for index, value in zip(counts[0], counts[1]):
        result[tuple(index)] = value
    return result / result.sum()
'''


def empirical_distribution(a: np.array):
    """Empirical discrete distribution for arbitrary dimensions"""
    A = a
    if len(a.shape) == 1:
        A = np.reshape(a, (a.shape[0], 1))
    result = np.zeros(A.shape[1]*[2])
    counts = np.unique(A, return_counts=True, axis=0)
    for index, value in zip(counts[0], counts[1]):
        result[tuple(index)] = value
    return result / result.sum()