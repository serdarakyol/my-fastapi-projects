from numba import njit, prange
from numpy import zeros, float64, int32, sqrt, array
from json import load

@njit('float64(int8[::1], int8[::1])')
def custom_cosine_similarity(a:array,b:array) -> array:
    """
    Calculate cosine similarity based on logical operation

    Return: Similarity
    """
    # Large safe integer type (int16 is less safe but certainly faster)
    dt = int32(0)
    for i in range(a.size):
        dt += a[i] & b[i]
    
    if dt == 0:
        return 0.0

    sa, sb = int32(0), int32(0)
    for i in range(a.size):
        sa += a[i]
        sb += b[i]
    return dt / sqrt(sa * sb)

@njit('float64[:](int8[:,::1], int8[::1])', parallel=True)
def calculate_similarity_parallel(multiple_item, single_item):
    """
    Paralel processing on numpy array

    Return: All similarity scores
    """
    n = multiple_item.shape[0]
    scores = zeros(n, float64)
    for i in prange(n):
        scores[i] = custom_cosine_similarity(single_item, multiple_item[i])
    return scores


def load_json(path):
    """
    Load json data

    Return: json object
    """
    # read meta data
    with open(path, 'r') as fp:
        data = load(fp)
        return data
